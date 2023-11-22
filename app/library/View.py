from uuid import uuid4
from datetime import datetime, timedelta
from ..auth import User
from .Organization import Organization
from .Event import Event
from .Room import Room


class View:
    def __init__(self, owner: User):
        self.owner = owner
        self.queries = {}

    def add_query(self, organization: Organization, **kw: dict) -> str:
        query_id = str(uuid4())
        self.queries[query_id] = {"organization": organization, "kw": kw}
        return query_id

    def del_query(self, query_id: str):
        del self.queries[query_id]

    def execute_queries(self, start_time: datetime, end_time: datetime):
        results = []
        for each_query in self.queries:
            organization: Organization = each_query["organization"]
            results.append(organization.query(**each_query["kw"]))

        datetime_filtered_query_results = []
        for each_query_result in results:
            for each_assignment in each_query_result:
                event: Event = each_assignment[0]
                event_start_time: datetime = each_assignment[2]

                if (
                    event_start_time >= start_time
                    and event_start_time + timedelta(minutes=event.duration) <= end_time
                ):
                    datetime_filtered_query_results.append(each_assignment)

        return datetime_filtered_query_results

    def room_view(self, start_time: datetime, end_time: datetime):
        datetime_filtered_query_results = self.execute_queries(
            start_time=start_time, end_time=end_time
        )

        room_view_dict = {}
        for each_assignment in datetime_filtered_query_results:
            location: Room = each_assignment[1]

            if location.name not in room_view_dict:
                room_view_dict[location.name] = []

            room_view_dict[location.name].append(each_assignment)

        return room_view_dict

    def day_view(self, start_time: datetime, end_time: datetime):
        datetime_filtered_query_results = self.execute_queries(
            start_time=start_time, end_time=end_time
        )

        day_view_dict = {}
        for each_assignment in datetime_filtered_query_results:
            start_time: datetime = each_assignment[2]

            date = start_time.strftime("%Y-%m-%d")

            if date not in day_view_dict:
                day_view_dict[date] = []

            day_view_dict[date].append(each_assignment)

        return day_view_dict
