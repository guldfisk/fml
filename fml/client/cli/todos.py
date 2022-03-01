import typing as t

import click

from fml.client import output
from fml.client.cli.common import AliasedGroup, main, split_text_option, force_option, get_default_project
from fml.client.client import Client
from fml.client.dtmath.parse import DTMParseException
from fml.client.output import show_points


@main.group('todo', cls = AliasedGroup)
def todo_service() -> None:
    """
    Keep track of stuff to do.
    """
    pass


@todo_service.command(name = 'new')
@split_text_option('text')
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--priority', '-i', default = None, type = str, help = 'Priority.')
@click.option('--tag', '-t', default = (), type = str, help = 'Tags.', multiple = True)
@click.option('--parent', '-a', default = (), type = str, help = 'Parent.', multiple = True)
@force_option
def new_todo(
    text: t.Sequence[str],
    project: t.Optional[str],
    priority: t.Optional[str],
    tag: t.Sequence[str],
    parent: t.Sequence[str],
    force: bool,
) -> None:
    """
    Create new todo.
    """
    if len(text) > 1 and not force:
        from fml.client.dtmath.parse import DTMParser
        try:
            DTMParser().parse(text[-1])
        except (DTMParseException, ValueError, TypeError):
            pass
        else:
            if not click.confirm('This looks like an alarm. Continue?', default = True):
                return
    output.print_todo(
        Client().new_todo(
            ' '.join(text),
            project = get_default_project(project),
            priority = priority,
            tags = tag,
            parents = parent,
        )
    )


@todo_service.command(name = 'modify')
@click.argument('todo', type = str, required = True)
@click.argument('description', type = str, required = False)
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
def modify_todo_description(
    todo: str,
    description: t.Optional[str],
    project: t.Optional[str],
) -> None:
    """
    Modify todo description.
    """
    client = Client()
    project = get_default_project(project)
    if description is None:
        existing_todo = client.get_todo(todo, project = project)
        description = click.edit(existing_todo.text)
        if description is None:
            print('aborted')
            return
        description = description.rstrip('\n')
    output.print_todo(
        Client().modify_todo_description(todo, description, project = project)
    )


@todo_service.command(name = 'com')
@click.argument('todo', type = str, required = True)
@click.argument('comment', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
def comment_todo(
    todo: str,
    comment: str,
    project: t.Optional[str],
) -> None:
    """
    Add comment to todo.
    """
    output.print_todo(
        Client().comment_todo(todo, comment, project = get_default_project(project))
    )


@todo_service.command(name = 'cancel')
@split_text_option()
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
def cancel_todo(target: t.Sequence[str], project: t.Optional[str] = None) -> None:
    """
    Cancel todo. Target is either id, partial text of todo or "l" for last todo.
    """
    output.print_todo(Client().cancel_todo(' '.join(target), get_default_project(project)))


@todo_service.command(name = 'wait')
@split_text_option()
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
def toggle_todo_wait(target: t.Sequence[str], project: t.Optional[str] = None) -> None:
    """
    Toggle todo waiting status. Target is either id, partial text of todo or "l" for last todo.
    """
    output.print_todo(Client().toggle_todo_waiting(' '.join(target), get_default_project(project)))


@todo_service.command(name = 'finish')
@split_text_option()
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
def finish_todo(target: t.Sequence[str], project: t.Optional[str] = None) -> None:
    """
    Finish todo. Target is either id, partial text of todo or "l" for last todo.
    """
    output.print_todo(Client().finish_todo(' '.join(target), get_default_project(project)))


@todo_service.command(name = 'list')
@click.option(
    '--history',
    '-h',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include non-pending todos.'
)
@click.option(
    '--limit',
    '-l',
    default = 25,
    type = int,
    help = 'Maximum number of top level todos to fetch when fetching history.',
    show_default = True,
)
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
@click.option('--tag', '-t', type = str, help = 'Filter on tag.')
@click.option(
    '--query',
    '-q',
    type = str,
    help = 'Filter on text. This also disables priority filtering. Specify minimum-priority to override this.',
)
@click.option(
    '--state',
    '-s',
    type = str,
    help = 'Filter on state.',
)
@click.option(
    '--order-by',
    '-o',
    type = str,
    help = 'Order by fields.',
    multiple = True,
)
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option(
    '--flat',
    '-f',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Dont show task children',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
@click.option(
    '--no-comments',
    '-c',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Dont show comments',
)
def list_todos(
    history: bool = False,
    limit: int = 25,
    **kwargs,
) -> None:
    """
    List pending todos.
    """
    kwargs['project'] = get_default_project(kwargs['project'])
    if kwargs['query'] and kwargs['minimum_priority'] is None:
        kwargs['ignore_priority'] = True
    no_comments = kwargs.pop('no_comments')
    output.print_todos(
        Client().todo_history(limit = limit, **kwargs)
        if history else
        Client().active_todos(**kwargs),
        show_comments = not no_comments,
    )


@todo_service.command(name = 'burndown')
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', type = str, help = 'Filter on tag.')
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
@click.option(
    '--last-n-days',
    '-n',
    default = 128,
    type = int,
    help = 'Data from at most n previous days.',
    show_default = True,
)
def todos_burn_down(
    project: t.Optional[str],
    tag: t.Optional[str],
    all_tasks: bool,
    ignore_priority: bool,
    minimum_priority: t.Optional[str],
    last_n_days: int,
) -> None:
    """
    Show todo burndown chart.
    """
    show_points(
        Client().todo_burn_down(
            project = get_default_project(project),
            tag = tag,
            all_tasks = all_tasks,
            ignore_priority = ignore_priority,
            minimum_priority = minimum_priority,
            last_n_days = last_n_days,
        ),
        title = 'ToDo Burndown',
        y_label = 'ToDo Qty.',
    )


@todo_service.command(name = 'throughput')
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', type = str, help = 'Filter on Tag.')
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
@click.option(
    '--last-n-days',
    '-n',
    default = 128,
    type = int,
    help = 'Data from at most n previous days.',
    show_default = True,
)
def todos_throughput(
    project: t.Optional[str],
    tag: t.Optional[str],
    all_tasks: bool,
    ignore_priority: bool,
    minimum_priority: t.Optional[str],
    last_n_days: int,
) -> None:
    """
    Show todo throughput chart.
    """
    show_points(
        Client().todo_throughput(
            project = get_default_project(project),
            tag = tag,
            all_tasks = all_tasks,
            ignore_priority = ignore_priority,
            minimum_priority = minimum_priority,
            last_n_days = last_n_days,
        ),
        title = 'ToDo Throughput',
        y_label = 'ToDo/Day',
    )


@todo_service.group('tag', cls = AliasedGroup)
def tag_service() -> None:
    """
    Todo tags.
    """
    pass


@tag_service.command(name = 'list')
def list_tags() -> None:
    """
    List tags.
    """
    output.print_tags(Client().list_tags())


@tag_service.command(name = 'new')
@split_text_option()
def create_tag(
    tag: t.Sequence[str],
) -> None:
    """
    Create a new tag
    """
    Client().create_tag(' '.join(tag))
    print('ok')


@tag_service.command(name = 'add')
@click.argument('todo', type = str, required = True)
@click.argument('tag', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option(
    '--recursive',
    '-r',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Add tag to all children recursively.',
)
def tag_todo(
    todo: str,
    tag: str,
    project: t.Optional[str],
    recursive: bool = False,
) -> None:
    """
    Tag todo. Target is either id, partial text of todo or "l" for last todo.
    """
    output.print_todo(
        Client().tag_todo(
            todo = todo,
            tag = tag,
            project = get_default_project(project),
            recursive = recursive,
        )
    )


@todo_service.command(name = 'dep')
@click.argument('parent', type = str, required = True)
@click.argument('task', type = str, required = True)
def register_dependency(
    parent: str,
    task: str,
) -> None:
    """
    Register task as subtask of other task
    """
    output.print_todo(
        Client().register_dependency(parent, task)
    )


@todo_service.group('project', cls = AliasedGroup)
def project_service() -> None:
    """
    Todo projects.
    """
    pass


@project_service.command(name = 'list')
def list_projects() -> None:
    """
    List projects.
    """
    output.print_projects(
        Client().list_projects()
    )


@project_service.command(name = 'new')
@click.argument('name', type = str, required = True)
def create_project(
    name: str,
) -> None:
    """
    Create a new project
    """
    output.print_project(
        Client().create_project(name)
    )


@project_service.command(name = 'mod')
@click.argument('project', type = str, required = True)
@click.argument('level', type = str, required = True)
def modify_project_default_priority_filter(
    project: str,
    level: str,
) -> None:
    """
    Modify default priority level for new todos
    """
    output.print_project(
        Client().modify_project_default_priority_filter(project, None if level.lower() == 'none' else level),
    )


@todo_service.group('priority', cls = AliasedGroup)
def priority_service() -> None:
    """
    Todo priorities.
    """
    pass


@priority_service.command(name = 'new')
@split_text_option('name')
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--level', '-l', default = 0, type = int, help = 'Level.')
def new_priority(
    name: t.Sequence[str],
    project: str,
    level: int,
) -> None:
    """
    Create a new priority.
    """
    output.print_priority(
        Client().new_priority(
            name = ' '.join(name),
            level = level,
            project = get_default_project(project),
        )
    )


@priority_service.command(name = 'swap')
@click.argument('first', type = str, required = True)
@click.argument('second', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Project.')
def swap_priority_levels(
    first: str,
    second: str,
    project: t.Optional[str],
) -> None:
    """
    Create priority levels of priorities.
    """
    output.print_priorities(
        Client().swap_priority_levels(
            first = first,
            second = second,
            project = get_default_project(project),
        )
    )


@priority_service.command(name = 'list')
@click.option('--project', '-p', type = str, help = 'Project.')
def list_priorities(project: str) -> None:
    """
    List priorities.
    """
    output.print_priorities(
        Client().list_priorities(project = get_default_project(project))
    )


@priority_service.command(name = 'modify')
@click.argument('todo', type = str, required = True)
@click.argument('priority', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
@click.option(
    '--recursive',
    '-r',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Change priority of all children recursively.',
)
def change_priority(
    todo: str,
    priority: str,
    project: t.Optional[str],
    recursive: bool = False,
) -> None:
    """
    Modify todo priority.
    """
    output.print_todo(
        Client().modify_todo_priority(
            todo,
            priority,
            project = get_default_project(project),
            recursive = recursive,
        )
    )
