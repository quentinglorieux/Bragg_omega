import requests


class Wavemeter:
    """
    Wavemeter driver to fetch frequency data from an HTTP API.
    """

    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initializes the Wavemeter.

        Args:
            base_url (str): Base URL of the wavemeter API.
        """
        self.base_url = base_url

    def get_frequency(self, channel: int = 3):
        """
        Fetches the laser frequency from the wavemeter.

        Args:
            channel (int): The wavemeter channel to read from (default: 3).

        Returns:
            float or None: The measured frequency in Hz, or None if an error occurs.
        """
        try:
            response = requests.get(f"{self.base_url}/api/freq/{channel}", timeout=5)
            response.raise_for_status()  # Raise an error for HTTP issues

            data = response.json()
            if "frequency" in data:
                print(f"✔ Wavemeter Channel {channel}: {data['frequency']} Hz")
                return data["frequency"]
            else:
                print("Unexpected response format:", data)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching frequency from Wavemeter: {e}")
            return None