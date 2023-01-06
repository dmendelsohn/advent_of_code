use std::cmp::{min, Ordering};

#[derive(Clone, Debug)]
enum PacketItem {
    Packet(Box<Packet>),
    Data(usize),
}

impl PacketItem {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (PacketItem::Packet(self_packet), PacketItem::Packet(other_packet)) => {
                self_packet.as_ref().cmp(other_packet.as_ref())
            }
            (PacketItem::Packet(self_packet), PacketItem::Data(other_value)) => {
                let other_packet = Packet {
                    items: vec![PacketItem::Data(*other_value)],
                };
                self_packet.as_ref().cmp(&other_packet)
            }
            (PacketItem::Data(self_value), PacketItem::Packet(other_packet)) => {
                let self_packet = Packet {
                    items: vec![PacketItem::Data(*self_value)],
                };
                self_packet.cmp(other_packet.as_ref())
            }
            (PacketItem::Data(self_value), PacketItem::Data(other_value)) => {
                self_value.cmp(other_value)
            }
        }
    }
}

#[derive(Clone, Debug)]
struct Packet {
    items: Vec<PacketItem>,
}

impl Packet {
    fn parse(text: &str) -> Self {
        let (packet, next_idx) = Packet::parse_partial(text, 0);
        assert_eq!(next_idx, text.len());
        packet
    }

    // Return packet starting at start_idx and idx of remaining str after parsed packet
    fn parse_partial(text: &str, start_idx: usize) -> (Self, usize) {
        assert_eq!(text.chars().nth(start_idx), Some('['));
        let mut items = vec![];
        let mut current_idx = start_idx + 1;
        loop {
            // Parse next packet item, updating current_idx
            match text.chars().nth(current_idx).unwrap() {
                '[' => {
                    let (packet_item, new_idx) = Packet::parse_partial(text, current_idx);
                    items.push(PacketItem::Packet(Box::new(packet_item)));
                    current_idx = new_idx;
                }
                '0'..='9' => {
                    let mut data_string = String::new();
                    while text.chars().nth(current_idx).unwrap().is_numeric() {
                        data_string.push(text.chars().nth(current_idx).unwrap());
                        current_idx += 1;
                    }
                    items.push(PacketItem::Data(data_string.parse::<usize>().unwrap()));
                }
                ']' => {} // Occurs when we have an empty packet, return handled below
                _ => {
                    panic!("Unexpected start char of packet item")
                }
            }

            // Determine if there is another item in this packet or if we're done
            match text.chars().nth(current_idx).unwrap() {
                ',' => current_idx += 1, // Move on to next packet item
                ']' => break,
                _ => panic!("Unexpected char after packet item"),
            }
        }

        (Packet { items }, current_idx + 1)
    }

    fn cmp(&self, other: &Self) -> Ordering {
        for index in 0..min(self.items.len(), other.items.len()) {
            // Element-wise comparison, stopping at first non-equal element
            match self.items[index].cmp(&other.items[index]) {
                Ordering::Greater => return Ordering::Greater,
                Ordering::Less => return Ordering::Less,
                Ordering::Equal => continue,
            };
        }
        // If all elements are equal up to common length, compare lengths
        self.items.len().cmp(&other.items.len())
    }
}

fn parse_input(input: &str) -> Vec<(Packet, Packet)> {
    let mut result = vec![];
    for pair_text in input.split("\n\n") {
        if let [first_line, second_line] = pair_text.lines().collect::<Vec<_>>()[..] {
            result.push((Packet::parse(first_line), Packet::parse(second_line)));
        }
    }
    result
}

fn part1(input: &str) -> String {
    let packet_pairs = parse_input(input);
    let mut result = 0;
    for (idx, packet_pair) in packet_pairs.iter().enumerate() {
        if let Ordering::Less = packet_pair.0.cmp(&packet_pair.1) {
            result += idx + 1
        }
    }
    result.to_string()
}

fn part2(input: &str) -> String {
    // Flatten into a single vector of packets
    let mut packets: Vec<Packet> =
        parse_input(input)
            .into_iter()
            .fold(Vec::new(), |mut array, c| {
                array.push(c.0);
                array.push(c.1);
                array
            });

    // Add the divider packets
    let divider_2 = Packet {
        items: vec![PacketItem::Packet(Box::new(Packet {
            items: vec![PacketItem::Data(2)],
        }))],
    };
    let divider_6 = Packet {
        items: vec![PacketItem::Packet(Box::new(Packet {
            items: vec![PacketItem::Data(6)],
        }))],
    };
    packets.push(divider_2.clone());
    packets.push(divider_6.clone());

    packets.sort_by(|a, b| a.cmp(b));

    // Find the index of the packets (note that we do 1-indexing)
    let divider_2_index = packets
        .iter()
        .position(|packet| packet.cmp(&divider_2) == Ordering::Equal)
        .unwrap()
        + 1;
    let divider_6_index = packets
        .iter()
        .position(|packet| packet.cmp(&divider_6) == Ordering::Equal)
        .unwrap()
        + 1;

    (divider_2_index * divider_6_index).to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
