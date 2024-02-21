from locust import HttpUser, task, between

from utils import loadClubs, loadCompetitions


class LocustTestServer(HttpUser):
    """
    Locust test user for simulating user behavior on the GUDLFT Registration
    Server.
    """

    wait_time = between(1, 5)
    competition = loadCompetitions()[0]
    club = loadClubs()[0]

    def on_start(self):
        """
        Called when a Locust user starts before any task is scheduled.
        """

        self.client.get("/", name=".index")
        self.client.post("/showSummary", data={'email': self.club["email"]},
                         name=".show_summary")

    @task
    def getBooking(self):
        """
        Task to simulate a GET request for booking a place in a competition.
        """

        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="book")

    @task
    def postBooking(self):
        """
        Task to simulate a POST request for purchasing places in a competition.
        """

        self.client.post(
            "/purchasePlaces", data={"places": 0, "club": self.club["name"],
                                     "competition": self.competition["name"]},
            name="purchasePlaces")

    @task
    def getBoard(self):
        """
        Task to simulate a GET request for viewing the scoreboard.
        """

        self.client.get("/scoreboard", name="scoreboard")
