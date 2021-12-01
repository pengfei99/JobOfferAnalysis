import datetime

from offres_emploi import Api
from offres_emploi.utils import dt_to_str_iso


class PoleEmploiConnector:
    def __init__(self, client_id: str, client_secret: str):
        self.client = Api(client_id=client_id,
                          client_secret=client_secret)

    def get_search_result_by_range(self, params: dict, range_min: int, range_max: int):
        # add range to filter
        range_str = f"{str(range_min)}-{str(range_max)}"
        params["range"] = range_str
        response = self.client.search(params=params)
        return response["resultats"]

    def get_all_search_result(self, params: dict):
        response = self.client.search(params=params)
        total_response_num = int(response["Content-Range"]["max_results"])
        total_result = []
        index = 0
        while total_response_num > 150:
            total_response_num = total_response_num - 150
            tmp = self.get_search_result_by_range(params, index, index + 149)
            index = index + 150
            for item in tmp:
                total_result.append(item)
        return total_result


def main():
    # build client api
    id = "PAR_getjobs_9758a500d4c1f19834da4f62e3eedf94ff3ebf59cc5b38ad55fb0e96de9a5826"
    secret = "903830b3dc3d9a6376f58eb12cb2bfe3c15ef7de4e45a662a531afcbd624b4bb"
    client = PoleEmploiConnector(id, secret)

    # build search params
    start_dt = datetime.datetime(2020, 12, 1, 12, 30)
    end_dt = datetime.datetime.today()
    keyword = "data"
    params = {
        "motsCles": keyword,
        'minCreationDate': dt_to_str_iso(start_dt),
        'maxCreationDate': dt_to_str_iso(end_dt),
        # add filter to filter job by department
        # 'department':'973',
    }

    # get search result
    total = client.get_all_search_result(params)
    print(f"total result: {len(total)}")


if __name__ == "__main__":
    main()
