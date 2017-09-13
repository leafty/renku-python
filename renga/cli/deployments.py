# -*- coding: utf-8 -*-
#
# Copyright 2017 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Interact with the deployment service."""

import click

from renga.cli._options import option_endpoint

from ..models._tabulate import tabulate
from ._client import from_config
from ._config import with_config


@click.group()
def contexts():
    """Manage execution contexts."""


@contexts.command()
@option_endpoint
@with_config
def list(config, endpoint):
    """List all contexts."""
    client = from_config(config, endpoint=endpoint)
    contexts = client.contexts
    click.echo(tabulate(contexts, headers=contexts.Meta.headers))


@contexts.command()
@click.argument('image')
@click.option('--command', '-c', help='Command to run in the container.')
@click.option(
    '--labels',
    '-l',
    multiple=True,
    help='Labels to add to the container.')
@click.option(
    '--ports',
    '-p',
    multiple=True,
    help='Ports to expose in the container.')
@option_endpoint
@with_config
def create(config, image, ports, command, labels, endpoint):
    """Create an execution context."""
    project_config = config.get('project', {})
    project_vertex_id = project_config.get('endpoints', {}).get(
        endpoint, {}).get('vertex_id')

    client = from_config(config, endpoint=endpoint)

    spec = {
        'command': command,
        'image': image,
        'labels': labels or [],
        'ports': ports or [],
    }

    if project_vertex_id:
        spec['labels'].append(
            'renga.project.vertex_id={0}'.format(project_vertex_id))

        client.api.headers['Renga-Projects-Project'] = project_vertex_id

    context = client.contexts.create(spec)
    click.echo(context.id)
    return context


@contexts.command()
@click.argument('context_id')
@click.argument('engine')
@option_endpoint
@with_config
def run(config, context_id, engine, endpoint):
    """Run an execution context."""
    client = from_config(config, endpoint=endpoint)
    execution = client.contexts[context_id].run(engine=engine)
    click.echo(execution.id)


@click.group()
def executions():
    """Manage executions."""


@executions.command(name='list')
@click.argument('context_id')
@option_endpoint
@with_config
def list_executions(config, context_id, endpoint):
    """Show the executions of a context."""
    client = from_config(config, endpoint=endpoint)
    executions = client.contexts[context_id].executions
    click.echo(tabulate(executions, headers=executions.Meta.headers))


@executions.command()
@click.argument('context_id')
@click.argument('execution_id')
@option_endpoint
@with_config
def ports(config, context_id, execution_id, endpoint):
    """Show the port and host mapping of an execution."""
    client = from_config(config, endpoint=endpoint)
    execution = client.contexts[context_id].executions[execution_id]
    click.echo(execution.ports)
