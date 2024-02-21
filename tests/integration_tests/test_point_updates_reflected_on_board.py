import server
from server import app


class TestPointsUpdate:
    """
    Unit test class for testing points update functionality.
    """

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "john@simplylift.co",
            "points": "13"
        }
    ]

    def setup_method(self):
        """
        Setup method to initialize test data for competitions and clubs.
        """

        server.competitions = self.competition
        server.clubs = self.club

    def testPointsUpdate(self):
        """
        Test method for checking points update after purchasing places.
        """

        # Store club points before purchasing places
        clubPointsBefore = int(self.club[0]["points"])
        placesBooked = 1

        # Simulate a purchase of places
        self.client.post(
            "/purchasePlaces", data={
                "places": placesBooked, "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]})

        # Retrieve the updated scoreboard
        result = self.client.get("/scoreboard")
        print(result)

        # Assertions to check if the points update is reflected in the
        # scoreboard
        assert result.status_code == 200
        assert f"<td>{self.club[0]['name']}</td>" in result.data.decode()
        assert f"<td>{clubPointsBefore - placesBooked}</td>" in result.data.decode()
