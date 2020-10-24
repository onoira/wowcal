# wowcal.py

Utility for catalogueing and comparing calendar systems in roleplay settings.

Available calendars:

- [onoira/calendars-wow](https://github.com/onoira/calendars-wow)

## Installation

    pip3 install "git+https://github.com/onoira/wowcal"
    wowcal --help

## Contributing

    # Clone the repository:
    git clone https://github.com/onoira/wowcal
    cd wowcal

    # Install in editable mode:
    pip3 install -e .

    # Begin coding!

If you would like to make your own calendars: refer to the [schema](schema.json), or an existing calendar list. You can check your file against the schema using the included validation script:

    pip3 install -e ".[Validation]"
    validate.py path/to/file.yml

## License

[MIT](LICENSE)
