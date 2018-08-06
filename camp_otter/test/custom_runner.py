from django.test.runner import DiscoverRunner
from django.db import connections
import django.test.utils as utils


class CampOtterRunner(DiscoverRunner):
    # override the setup_databases method to use the tiger database as-is, without creating a test database.
    def setup_databases(self, **kwargs):

        test_databases, mirrored_aliases = utils.get_unique_databases_and_mirrors()

        test_databases.popitem()  # this works because the tiger database is the last in the ordered dict.  TODO: make this more explicit

        old_names = []

        for signature, (db_name, aliases) in test_databases.items():
            first_alias = None
            for alias in aliases:
                connection = connections[alias]
                old_names.append((connection, db_name, first_alias is None))

                # Actually create the database for the first connection
                if first_alias is None:
                    first_alias = alias
                    connection.creation.create_test_db(
                        verbosity=self.verbosity,
                        autoclobber=not self.interactive,
                        keepdb=self.keepdb,
                        serialize=connection.settings_dict.get('TEST', {}).get('SERIALIZE', True),
                    )
                    if self.parallel > 1:
                        for index in range(self.parallel):
                            connection.creation.clone_test_db(
                                suffix=str(index + 1),
                                verbosity=self.verbosity,
                                keepdb=self.keepdb,
                            )
                # Configure all other connections as mirrors of the first one
                else:
                    connections[alias].creation.set_as_test_mirror(connections[first_alias].settings_dict)

        # Configure the test mirrors.
        for alias, mirror_alias in mirrored_aliases.items():
            connections[alias].creation.set_as_test_mirror(
                connections[mirror_alias].settings_dict)

        if self.debug_sql:
            for alias in connections:
                connections[alias].force_debug_cursor = True

        return old_names

