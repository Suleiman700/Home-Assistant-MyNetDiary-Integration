"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import logging
_LOGGER = logging.getLogger(__name__)

import re
import requests
from bs4 import BeautifulSoup

MyNetDiary_URL = "<YOUR COMMUNITY LINK HERE>"

def get_current_weight():
    current_weight = None
    start_weight = None
    lost_so_far = None

    try:
        """Fetch the current weight from the website."""
        # Send a GET request to the URL
        response = requests.get(MyNetDiary_URL)

        if response.status_code == 200:
            # Extract the HTML content
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Find the <ul> element containing the weight information
            weight_ul = soup.find("ul")

            # Extract the list items from the <ul> element
            weight_items = weight_ul.find_all("li")

            # Loop through the list items to find the current weight
            for item in weight_items:
                text = item.get_text()
                if "Current weight" in text:
                    current_weight = text.split(":")[1].strip()

                    # Remove non-numeric characters using regular expressions
                    numeric_weight = re.sub(r"[^\d.]", "", current_weight)

                    current_weight = float(numeric_weight)

                if "Start weight" in text:
                    current_start_weight = text.split(":")[1].strip()
                    start_weight = current_start_weight
                if "Lost so far" in text:
                    lost_so_far = text.split(":")[1].strip()

    except Exception as e:
        print(e)

    response = dict()
    response['current_weight'] = current_weight
    response['start_weight'] = start_weight
    response['lost_so_far'] = lost_so_far
    return response

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([MyNetDiaryCurrentWeight(), MyNetDiaryStartWeight(), MyNetDiaryLostSoFar()])


class MyNetDiaryCurrentWeight(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "MyNetDiary current weight"
    _attr_native_unit_of_measurement = "kg"
    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "weight_sensor"  # Unique ID for the sensor

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        # Fetch data
        data = get_current_weight()
        current_weight = data['current_weight']

        # If weight is available, update the sensor value
        if current_weight is not None:
            # Convert the string to a floating-point number
            weight_value = float(current_weight)
            self._attr_native_value = weight_value
        else:
            self._attr_native_value = -1

class MyNetDiaryStartWeight(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "MyNetDiary start weight"
    _attr_native_unit_of_measurement = None  # Remove the unit of measurement for text sensor
    _attr_device_class = None  # Set device class to None for a generic text sensor
    _attr_state_class = None  # Remove the state class since it's not applicable for text sensors
    _attr_unique_id = "start_weight_sensor"  # Unique ID for the sensor

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        # Fetch data
        data = get_current_weight()
        start_weight = data['start_weight']


        # If weight is available, update the sensor value
        if start_weight is not None:
            self._attr_native_value = start_weight
        else:
            self._attr_native_value = 'Unavailable'

class MyNetDiaryLostSoFar(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "MyNetDiary lost so far"
    _attr_native_unit_of_measurement = None  # Remove the unit of measurement for text sensor
    _attr_device_class = None  # Set device class to None for a generic text sensor
    _attr_state_class = None  # Remove the state class since it's not applicable for text sensors
    _attr_unique_id = "lost_so_far_sensor"  # Unique ID for the sensor

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        # Fetch data
        data = get_current_weight()
        lost_so_far = data['lost_so_far']

        # If weight is available, update the sensor value
        if lost_so_far is not None:
            self._attr_native_value = lost_so_far
        else:
            self._attr_native_value = 'Unavailable'
