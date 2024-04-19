class ProtectedFieldSerializer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.should_show_protected_fields():
            self.make_protected_fields_write_only()

    def should_show_protected_fields(
        self,
    ):
        return False

    def make_protected_fields_write_only(
        self,
    ):
        if not hasattr(
            self.Meta,
            "protected_fields",
        ):
            return
        for field_name in self.Meta.protected_fields:
            self.fields[field_name].write_only = True


class WrapSerializerDataMixin:
    def get_wrap_key(self):
        return getattr(self.Meta, "wrap", "data")

    def get_unwrapped_fields(self):
        fields = getattr(
            self.Meta,
            "exclude_wrap_fields",
            [],
        )
        return list(fields)

    def to_representation(self, instance):
        wrap_key = self.get_wrap_key()
        data = super().to_representation(instance)
        if not isinstance(wrap_key, str):
            return data

        unwrapped_fields = self.get_unwrapped_fields()
        unwrapped_data = {
            field: data.pop(field)
            for field in unwrapped_fields
            if field in data
        }

        return {
            wrap_key: data,
            **unwrapped_data,
        }
