"""Module providing calls to the demo api."""

from typing import List
from urllib.parse import urljoin
import json
import requests


class DemoApi:
    """
    A simple demo class where the API logic is written

    :param username: user that connect to API
    :param password: password from the user
    :param token: token can be user instead of username/password
    :param uri: the endpoint of the API
    :raises HTTPError: if one occurred
    """

    def __init__(self, username: str, password: str, token: str, uri: str):
        self.uri = uri
        self.session = requests.session()
        self.__connect(username, password, token)

    def __connect(self, username: str, password: str, token: str):
        if token:
            self.session.headers.update({'X-Auth-Token': token})
        else:
            response = self.session.post(urljoin(self.uri, "token"), json={
                                         "username": username, "password": password})
            response.raise_for_status()
            self.session.headers.update({'X-Auth-Token': response.text})

    def reset(self, character: str) -> None:
        """
        Reset will remove character from the set of characters that are set

        :param character: character to reset
        :raises HTTPError: if one occurred
        """
        response = self.session.delete(
            urljoin(self.uri, f"character/{character}"))
        response.raise_for_status()

    def set(self, character: str, number: int) -> None:
        """
        Set the number on a character

        :param character: character to set
        :param number: the number that will be given to the character

        :raises HTTPError: if one occurred
        """
        response = self.session.put(
            urljoin(self.uri, f"character/{character}?number={number}"))
        response.raise_for_status()

    def update(self, character: str, number: int) -> None:
        """
        Update the number on a character

        :param character: character to update
        :param number: the number that will be given to the character

        :raises HTTPError: if one occurred
        """
        response = self.session.post(
            urljoin(self.uri, f"character/{character}?number={number}"))
        response.raise_for_status()

    def get(self, character: str) -> int:
        """
        Get the number that is set on a character

        :param character: character where you want the number from

        :returns: the number that will be given to the character
        :raises HTTPError: if one occurred
        """
        response = self.session.get(
            urljoin(self.uri, f"character/{character}"))
        response.raise_for_status()
        return json.loads(response.text)

    def list(self) -> List[str]:
        """
        Get the list of characters that are set

        :returns: the list of characters that have a number
        :raises HTTPError: if one occurred
        """
        response = self.session.get(urljoin(self.uri, "character"))
        response.raise_for_status()
        return json.loads(response.text)
