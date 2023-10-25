from dataclasses import dataclass, field, asdict
import panel as pn
import param

@dataclass
class SubModel:
    text1: str = param.String(default="", doc="First text field")
    text2: str = param.String(default="", doc="Second text field")
    text3: str = param.String(default="", doc="Third text field")
    option: str = param.Selector(objects=['Option 1', 'Option 2'], default='Option 1')

@dataclass
class Model:
    foo: list = field(default_factory=list)

class DynamicDashboard(param.Parameterized):
    file_path = param.String()
    add_button = param.Action(lambda x: x.add_row(), label='Add Row')

    def __init__(self, model, **params):
        super(DynamicDashboard, self).__init__(**params)
        self.model = model
        self.dynamic_controls = []

    def add_row(self):
        new_submodel = SubModel()
        self.model.foo.append(new_submodel)
        new_row = pn.Param(new_submodel, show_name=False, widgets={
            'text1': pn.widgets.TextInput,
            'text2': pn.widgets.TextInput,
            'text3': pn.widgets.TextInput,
            'option': pn.widgets.Select
        })

        remove_button = pn.widgets.Button(name='X', button_type='danger', width=50)
        remove_button.param.watch(lambda event: self.remove_row(new_row, new_submodel), 'clicks')

        self.dynamic_controls.append(pn.Row(remove_button, new_row))

    def remove_row(self, row, submodel):
        self.dynamic_controls.remove(row)
        self.model.foo.remove(submodel)

    def view(self):
        return pn.Column(
            pn.Row("File Path:", pn.panel(self.param.file_path)),
            pn.panel(self.param.add_button),
            *self.dynamic_controls
        )

if __name__ == "__main__":
    model = Model()
    dashboard = DynamicDashboard(model=model)
    pn.serve(dashboard.view)
