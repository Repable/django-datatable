#!/usr/bin/env python
# coding: utf-8
from django import template
from django.template import Context


register = template.Library()


class TableNode(template.Node):

    def __init__(self, table, template_name):
        self.template_name = template_name
        self.table = template.Variable(table)

    def render(self, context):
        table = self.table.resolve(context)
        context = Context({'table': table})
        t = template.loader.get_template(self.template_name)
        return t.render(context)


@register.tag
def render_table(parser, token):
    try:
        tag, table, template_name = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table, template_name)


@register.tag
def render_simple_table(parser, token):
    try:
        tag, table, template_name = token.split_contents()
    except ValueError:
        msg = '%r tag requires a arguments {% render_table table template_name %]' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table, template_name)
