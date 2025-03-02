from django_filters.widgets import LinkWidget as DjangoFiltersLinkWidget


class LinkWidget(DjangoFiltersLinkWidget):
    def option_string(self):
        return '<li><a%(attrs)s class="custom-link" href="?%(query_string)s">%(label)s</a></li>'