import omero.cli
import omero.gateway

def get_images(project):
    for dataset in project.listChildren():
        for image in dataset.listChildren():
            yield image

with omero.cli.cli_login() as c:
    conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
    project = conn.getObject("Project", attributes={'id': 2701})

    to_delete = []
    for image in get_images(project):
        for ann in image.listAnnotations():
            for k,v  in ann.getValue():
                if k == 'MinSampleValue':
                    to_delete.append(ann)
                    continue
    if to_delete:
        ids = [ann.getId() for ann in to_delete]
        print(f"Deleting annotations {ids}")
        conn.deleteObjects('Annotation', ids, wait=True)
