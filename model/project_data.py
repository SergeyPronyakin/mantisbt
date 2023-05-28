from sys import maxsize


class ProjectData:

    def __init__(self, project_name=None, description=None, id=None):
        self.project_name = project_name
        self.description = description
        self.id = id

    def __repr__(self):
        return "%s:%s:%s:" % (self.id, self.project_name, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.project_name == other.project_name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return int(maxsize)
