extern crate core;
extern crate queues;

use clap::{command, value_parser, Arg, ArgAction};
use std::{fs, process};

pub mod year2022;

fn main() {
    let matches = command!()
        .arg(
            Arg::new("year")
                .short('y')
                .long("year")
                .required(false)
                .default_value("2022")
                .value_parser(value_parser!(u32)),
        )
        .arg(
            Arg::new("day")
                .short('d')
                .long("day")
                .required(true)
                .value_parser(value_parser!(u8)),
        )
        .arg(
            Arg::new("example")
                .short('e')
                .long("example")
                .action(ArgAction::SetTrue),
        )
        .get_matches();
    let year = matches
        .get_one::<u32>("year")
        .expect("Year must be an integer");
    let day = matches
        .get_one::<u8>("day")
        .expect("Day must be an integer");
    let is_example = matches.get_flag("example");

    let input_path = format!(
        "../inputs/year{}/{}{:0>2}.txt",
        year,
        if is_example { "example" } else { "day" },
        day
    );
    let input = match fs::read_to_string(&input_path) {
        Ok(input) => input,
        Err(e) => {
            println!("Could not read file at {}: {}", &input_path, e);
            process::exit(1)
        }
    };

    println!(
        "Running with year={}. day={}, example={}",
        year, day, is_example
    );
    match (year, day) {
        (2022, 01) => year2022::day01::run(&input[..]),
        (2022, 02) => year2022::day02::run(&input[..]),
        (2022, 03) => year2022::day03::run(&input[..]),
        (2022, 04) => year2022::day04::run(&input[..]),
        (2022, 05) => year2022::day05::run(&input[..]),
        (2022, 06) => year2022::day06::run(&input[..]),
        (2022, 07) => year2022::day07::run(&input[..]),
        (2022, 08) => year2022::day08::run(&input[..]),
        (2022, 09) => year2022::day09::run(&input[..]),
        (2022, 10) => year2022::day10::run(&input[..]),
        (2022, 11) => year2022::day11::run(&input[..]),
        (2022, 12) => year2022::day12::run(&input[..]),
        (2022, 13) => year2022::day13::run(&input[..]),
        (2022, 14) => year2022::day14::run(&input[..]),
        _ => panic!("No solution defined for year={} day={}", year, day),
    }
}
