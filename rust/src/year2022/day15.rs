use lazy_static::lazy_static;
use regex::Regex;
use std::cmp::{max, min};
use std::collections::HashSet;

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Location {
    x: isize,
    y: isize,
}

impl Location {
    fn manhattan_distance(&self, other: &Location) -> isize {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

#[derive(Debug)]
struct Sensor {
    location: Location,
    nearest_beacon: Location,
}

impl Sensor {
    fn parse(text: &str) -> Self {
        lazy_static! {
            static ref RE: Regex = Regex::new(
                r"^Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)$"
            )
            .unwrap();
        }
        let caps = RE.captures(text).unwrap();
        let location = Location {
            x: caps.get(1).unwrap().as_str().parse::<isize>().unwrap(),
            y: caps.get(2).unwrap().as_str().parse::<isize>().unwrap(),
        };
        let nearest_beacon = Location {
            x: caps.get(3).unwrap().as_str().parse::<isize>().unwrap(),
            y: caps.get(4).unwrap().as_str().parse::<isize>().unwrap(),
        };
        Sensor {
            location,
            nearest_beacon,
        }
    }

    /// Get x range within beacon distance along specified horizontal line
    /// Return None if the horizontal line is entirely further than the beacon distance
    fn get_x_range_within_beacon_distance(&self, y: isize) -> Option<Range> {
        let y_dist = (self.location.y - y).abs();
        let maximum_x_dist = self.beacon_distance() - y_dist;
        if maximum_x_dist > 0 {
            let range = Range {
                low: self.location.x - maximum_x_dist,
                high: self.location.x + maximum_x_dist,
            };
            Some(range)
        } else {
            None
        }
    }

    fn beacon_distance(&self) -> isize {
        self.location.manhattan_distance(&self.nearest_beacon)
    }
}

/// Represents an inclusive range
#[derive(Clone, Copy, Debug, PartialEq)]
struct Range {
    low: isize,
    high: isize,
}

impl Range {
    fn size(&self) -> isize {
        self.high - self.low + 1
    }

    // Merge if the ranges are overlapping or adjacent, or else return None
    fn merge(&self, other: &Range) -> Option<Range> {
        if self.low > other.high + 1 || self.high < other.low - 1 {
            None
        } else {
            Some(Range {
                low: min(self.low, other.low),
                high: max(self.high, other.high),
            })
        }
    }
}

fn parse_input(input: &str) -> Vec<Sensor> {
    input.lines().map(|line| Sensor::parse(line)).collect()
}

fn get_beacons(sensors: &Vec<Sensor>) -> HashSet<Location> {
    HashSet::from_iter(sensors.iter().map(|sensor| sensor.nearest_beacon))
}

/// Merge the input ranges so that the output is disjoint
fn merge_ranges(mut ranges: Vec<Range>) -> Vec<Range> {
    ranges.sort_by_key(|range| range.low);
    let mut range_iter = ranges.iter();
    let mut current_range = match range_iter.next() {
        Some(range) => *range,
        None => return vec![],
    };

    // Build up disjoint ranges
    let mut disjoint_ranges: Vec<Range> = vec![];
    while let Some(next_range) = range_iter.next() {
        match current_range.merge(next_range) {
            // If overlap, merge next range into current range
            Some(overlap_range) => current_range = overlap_range,
            // If no overlap, push current range and replace it with the new range
            None => {
                disjoint_ranges.push(current_range);
                current_range = *next_range;
            }
        }
    }

    // Push last range
    disjoint_ranges.push(current_range);

    disjoint_ranges
}

fn is_covered(value: isize, ranges: &Vec<Range>) -> bool {
    ranges
        .iter()
        .find(|range| range.low <= value && value <= range.high)
        != None
}

fn part1(input: &str) -> String {
    // Gather inputs
    let sensors = parse_input(input);
    let beacons = get_beacons(&sensors);
    let y = if sensors.len() == 14 { 10 } else { 2000000 }; // Test case is different y

    // Calculate the x ranges at the specified y, and merge so they are disjoint
    let x_ranges = sensors
        .iter()
        .filter_map(|sensor| sensor.get_x_range_within_beacon_distance(y))
        .collect::<Vec<_>>();
    let disjoint_ranges = merge_ranges(x_ranges);

    // Count the total size, subtracting out known beacons
    let total_range_size: isize = disjoint_ranges.iter().map(|range| range.size()).sum();

    let beacons_included = beacons
        .iter()
        .map(|beacon| beacon.y == y && is_covered(beacon.x, &disjoint_ranges))
        .filter(|val| *val)
        .count() as isize;

    (total_range_size - beacons_included).to_string()
}

fn get_uncovered_x_for_y(sensors: &Vec<Sensor>, y: isize, window_size: isize) -> Option<isize> {
    let x_ranges = sensors
        .iter()
        .filter_map(|sensor| sensor.get_x_range_within_beacon_distance(y))
        .collect::<Vec<_>>();
    let disjoint_ranges = merge_ranges(x_ranges);
    match disjoint_ranges.len() {
        1 => {
            let range = disjoint_ranges[0];
            if range.low == 1 {
                Some(0)
            } else if range.high == window_size - 1 {
                Some(window_size)
            } else {
                None
            }
        }
        2 => {
            let first_range = disjoint_ranges[0];
            let second_range = disjoint_ranges[1];
            assert_eq!(first_range.high + 2, second_range.low);
            Some(first_range.high + 1)
        }
        _ => panic!(
            "Unexpectedly had {} ranges at y={}",
            disjoint_ranges.len(),
            y
        ),
    }
}

fn part2(input: &str) -> String {
    // Gather inputs
    let sensors = parse_input(input);
    let window_size: isize = if sensors.len() == 14 { 20 } else { 4000000 };

    for y in 0..=window_size {
        match get_uncovered_x_for_y(&sensors, y, window_size) {
            Some(x) => return (x * 4000000 + y).to_string(),
            None => continue,
        }
    }
    panic!("Could not find beacon");
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
