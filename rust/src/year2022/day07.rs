use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::{Rc, Weak};

#[derive(Debug)]
enum Command<'a> {
    Ls { output: &'a str },
    Cd { dirname: &'a str },
}

impl<'a> Command<'a> {
    fn from(text: &'a str) -> Self {
        if let Some(output) = text.strip_prefix("ls\n") {
            Command::Ls { output }
        } else if let Some(dirname) = text.strip_prefix("cd ") {
            if dirname.contains(char::is_whitespace) {
                panic!("Directory name cannot contain whitespace: {dirname}");
            }
            Command::Cd { dirname }
        } else {
            panic!("Could not parse command from text: {text}");
        }
    }
}

#[derive(Debug)]
struct Directory {
    parent: RefCell<Weak<Directory>>, // If None, this is the root directory
    contents: RefCell<Option<Contents>>, // If None, contents are unknown
}

impl Directory {
    fn get_parent_dir(&self) -> Rc<Directory> {
        self.parent
            .borrow()
            .upgrade()
            .expect("Cannot cd to parent if the directory is the root")
    }

    fn get_child_dir(&self, dirname: &str) -> Rc<Directory> {
        assert!(!dirname.contains(" "));
        self.contents
            .borrow()
            .as_ref()
            .unwrap()
            .directories
            .get(dirname)
            .expect("Could not find requested child directory")
            .clone()
    }
}

#[derive(Debug)]
struct Contents {
    files: HashMap<String, usize>,
    directories: HashMap<String, Rc<Directory>>,
}

fn add_contents_to_directory(directory: Rc<Directory>, ls_output: &str) {
    let mut contents = Contents {
        files: HashMap::new(),
        directories: HashMap::new(),
    };

    for line in ls_output.lines() {
        let parts: Vec<&str> = line.split(" ").collect();
        match parts[..] {
            ["dir", dirname] => {
                let subdir = Rc::new(Directory {
                    parent: RefCell::new(Weak::new()),
                    contents: RefCell::new(None), // Contents are initially unknown
                });
                *subdir.parent.borrow_mut() = Rc::downgrade(&directory);

                contents.directories.insert(String::from(dirname), subdir);
            }
            [filesize, filename] => {
                contents
                    .files
                    .insert(String::from(filename), filesize.parse::<usize>().unwrap());
            }
            _ => panic!("Unexpected line of file contents: {line}"),
        };
    }

    *directory.contents.borrow_mut() = Some(contents);
}

fn parse_input(input: &str) -> Vec<Command> {
    // Split into distinct command text and validate that we start with `cd /`
    let mut commands_iter = input.split("$").map(|c| c.trim());
    assert_eq!(commands_iter.next().unwrap(), ""); // No text before initial '$'
    assert_eq!(commands_iter.next().unwrap(), "cd /");

    // Parse each command
    commands_iter.map(|text| Command::from(text)).collect()
}

fn run_commands(commands: Vec<Command>) -> Rc<Directory> {
    // Initialize root directory and set it as our working dir
    let root_dir = Rc::new(Directory {
        parent: RefCell::new(Weak::new()), // No parent of the root dir
        contents: RefCell::new(None),      // Contents are initially unknown
    });
    let mut working_dir = root_dir.clone();

    // Execute commands one by one:
    for command in commands {
        match command {
            Command::Ls { output } => {
                if let Some(_) = *working_dir.contents.borrow() {
                    panic!("Redundant ls not supported when directory contents are known")
                }
                add_contents_to_directory(working_dir.clone(), output);
            }
            Command::Cd { dirname: ".." } => working_dir = working_dir.get_parent_dir(),
            Command::Cd { dirname } => working_dir = working_dir.get_child_dir(dirname),
        }
    }

    root_dir
}

/// Finds the size of the root directory
/// Also populates `result` with the sizes of all subdirectories (including the root)
fn get_directory_size(root: Rc<Directory>, result: &mut Vec<usize>) -> usize {
    // TODO: implement
    let contents = root
        .contents
        .take()
        .expect("Cannot analyze directory size when contents are unknown");
    let total_file_size = contents.files.values().sum::<usize>();
    let total_directory_size = contents
        .directories
        .values()
        .map(|dir| get_directory_size(dir.clone(), result))
        .sum::<usize>();
    let total_size = total_file_size + total_directory_size;
    result.push(total_size);
    total_size
}

fn part1(input: &str) -> String {
    let commands = parse_input(input);
    let root_dir = run_commands(commands);
    let mut directory_sizes: Vec<usize> = vec![];
    get_directory_size(root_dir.clone(), &mut directory_sizes);

    directory_sizes
        .into_iter()
        .filter(|size| *size <= 100_000)
        .sum::<usize>()
        .to_string()
}

fn part2(input: &str) -> String {
    let commands = parse_input(input);
    let root_dir = run_commands(commands);
    let mut directory_sizes: Vec<usize> = vec![];
    let used_space = get_directory_size(root_dir.clone(), &mut directory_sizes);
    let max_allowed_used_space: usize = 70_000_000 - 30_000_000;
    if used_space < max_allowed_used_space {
        panic!("No directories need to be deleted");
    }

    let required_dealloc = used_space - max_allowed_used_space;
    directory_sizes
        .into_iter()
        .filter(|size| *size >= required_dealloc)
        .min()
        .unwrap()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
