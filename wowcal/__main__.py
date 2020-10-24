from __future__ import annotations

import typing
import os.path as path
import click

from wowcal import models

CALENDARS_FILE = 'calendars.yml'


@click.group()
@click.option('--file', type=click.File(), default=CALENDARS_FILE,
    help=f"Defaults to '{CALENDARS_FILE}'."
)
@click.pass_context
def main(ctx:click.Context, file:IO[str]):
    index = models.Index.from_file(file)
    ctx.ensure_object(dict)
    ctx.obj['_index'] = index

@main.command('list', help="List all calendar ids.")
@click.pass_context
def list_(ctx:click.Context):
    index = ctx.obj['_index']
    for system in index:
        print(system.id)

@main.command(help="Display calendar system details.")
@click.argument('id')
@click.pass_context
def show(ctx:click.Context, id:str):
    index = ctx.obj['_index']
    system = index.get_system(id)
    if not system:
        raise click.ClickException(f"no system for id '{id}'")

    # -------------------------------- fuckmyeyes -------------------------------- #

    s  = f"{'Name:':<12}{system.name}\n"
    s += f"{'Users:':<12}{', '.join(system.info.users)}\n"
    if system.info.initiator:
        s += f"{'Initiator:':<12}{system.info.initiator}\n"
    if system.info.namesake:
        s += f"{'Namesake:':<12}{system.info.namesake}\n"

    s += f"{'Year:':<12}{system.get_year(system.reference_year)}"
    if system.eras:
        s += f" ({system.reference_year})\n"
        s += "Eras:\n"
        for era_start, era_affix in system.eras.items():
            s += f"{' '*4}{era_start:<5}- {era_affix.name} ({era_affix.acronym})\n"
        s += f"{' '*4}{'...':<5}- {system.affix_positive.name} ({system.affix_positive.acronym})\n"
    else:
        s += '\n'
        if system.affix_negative:
            s += f"{'Prefix (+):' if system.affix_positive.is_prefix else 'Suffix (+):':<12}"
            s += f"{system.affix_positive.name} "
            s += f"({system.affix_positive.acronym[int(system.affix_positive.is_prefix):]})\n"

            s += f"{'Prefix (-):' if system.affix_negative.is_prefix else 'Prefix (-):':<12}"
            s += f"{system.affix_negative.name} "
            s += f"({system.affix_negative.acronym[int(system.affix_negative.is_prefix):]})\n"
        else:
            s += f"{'Affix:':<12}{system.affix_positive.name} ({system.affix_positive.acronym})\n"
    if system.info.succeeded_by:
        year = system.get_year(system.reference_year + system.info.succeeded_by[1])
        new_system = index.get_system(system.info.succeeded_by[0]).name
        s += f"Succeeded by: {new_system}, {year}\n"
    if system.info.notes:
        s += f"Notes:\n{system.info.notes}\n"

    click.echo(s)  # woot

@main.command(help="List equivalent year in other calendar systems.")
@click.argument('id')
@click.argument('year', type=click.INT)
@click.pass_context
def compare(ctx:click.Context, id:str, year:int):
    index = ctx.obj['_index']
    system = index.get_system(id)
    if not system:
        raise click.ClickException(f"no system for id '{id}'")

    offset = year - system.reference_year
    for system in index.systems:
        print(
            f'{system.name}:',
            f"{' '*4}{system.get_year(system.reference_year + offset)}",
            sep='\n'
        )


if __name__ == '__main__':
    main.main()
