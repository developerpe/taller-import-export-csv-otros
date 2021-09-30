import csv

from django.http import HttpResponse

from import_export import resources

from core.models import Author


def export_csv(request):
    """
    
    Native Export CSV

    # query
    queryset = Author.objects.all()
    
    # get fields of model
    options = Author._meta
    fields = [field.name for field in options.fields]
    # ['id', 'name', 'last_name']...
    # build response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename="authors.csv"'

    # writer
    writer = csv.writer(response)
    # writing header
    writer.writerow([options.get_field(field).verbose_name for field in fields])

    # writing data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    
    return response
    """


    # Import-Export library
    author_resource = resources.modelresource_factory(model=Author)()
    dataset = author_resource.export()
    response = HttpResponse(dataset.xls, content_type='text/xls')
    response['Content-Disposition'] = 'atachment; filename="author_library.xls"'
    return response



def import_csv(request):
    """

    Native Import CSV

    authors = []
    with open("ejemplo.csv", "r") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
        for row in data[1:]:
            authors.append(
                Author(
                    id=row[0],
                    name=row[1],
                    last_name=row[2],
                    nationality=row[3],
                    description=row[4],
                    state=row[5],
                    date_created=row[6]
                )
            )
    if len(authors) > 0:
        Author.objects.bulk_create(authors)
    
    return HttpResponse("Successfully imported")
    """

    # Import-Export library

    with open("ejemplo.csv", "r") as csv_file:
        import tablib

        author_resource = resources.modelresource_factory(model=Author)()
        dataset = tablib.Dataset(headers=[field.name for field in Author._meta.fields]).load(csv_file)
        result = author_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            author_resource.import_data(dataset, dry_run=False)
        return HttpResponse(
            "Successfully imported"
        )