# Client Finder

A Ruby command-line application to search clients from a JSON dataset and identify duplicate email entries. Designed with scalability, modularity, and testability in mind.

---

## Setup

1. **Install dependencies**

```bash
bundle install
```

2. **Make the script executable**

```bash
chmod +x bin/client_finder
```

3. **Run the application**

```bash
# Search clients by name (default field is `full_name`)
./bin/client_finder search Jane

# Search clients by email
./bin/client_finder search --field=email example.com

# Search using a different JSON file
./bin/client_finder search --file=other_clients.json Michael

# Find clients with duplicate email addresses
./bin/client_finder duplicates

```

## Features

- Search clients using a partial match on any specified field (default: full_name)

- Detect duplicate emails within the dataset

- Flexible file input via --file=your_data.json

-  Field selector via --field=field_name


## Running Tests

```bash
rspec
```

    Tests cover:

    - Partial match search on any field

    - Invalid field behavior

    - Duplicate detection

    - Edge and negative cases

    - JSON file loading

## Assumptions & Decisions

- The dataset is a flat JSON array with at least id, full_name, and email fields.

- All client fields are treated as strings for search purposes.

- Matching is case-insensitive and uses include? logic.

- CLI is preferred over a GUI/API for simplicity and speed in this challenge.

- The app is structured similarly to a real-world Rails service (with Client, ClientStore, SearchService).


## Example Usage

```bash
./bin/client_finder search --field=full_name "Jane"
./bin/client_finder search --field=email "@gmail.com"
./bin/client_finder duplicates
```

## Author

@jasonmag


## License

This project is licensed under the [MIT License](LICENSE).
