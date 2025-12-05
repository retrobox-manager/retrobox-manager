#!/usr/bin/python3
"""XML Helper"""

import os
import xml.etree.ElementTree as ET


class XmlHelper:
    """Class to help usage of XML"""

    @staticmethod
    def print_all_tags(
        xml_file_path: str
    ):
        """Show content"""

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Print all tags
        for elem in root.iter():
            print(f"Tag : {elem.tag}  |  Text : {elem.text!r}")

    @staticmethod
    def list_tag_values(
        xml_file_path: str,
        tag: str,
        parent_tag=None
    ):
        """List values for a tag from a XML file"""

        # Initialize result
        result = []

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # List values for the specified tag
        if parent_tag is None:
            result = [elem.text for elem in root.iter(tag)]
        else:
            for node in root.findall(f'.//{parent_tag}'):
                result.append(node.find(tag).text)

        return result

    @staticmethod
    def retrieve_node(
        xml_file_path: str,
        tag: str,
        field_id: str,
        field_value: str
    ) -> ET.Element:
        """Retrieve a node for the specified tag and field from a XML file"""

        # Initialize result
        result = None

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        for tag_node in root.findall(tag):
            field_node = tag_node.find(field_id)
            if field_node is not None and field_node.text == field_value:
                result = tag_node
                break

        return result

    @staticmethod
    def write_node(
        xml_file_path: str,
        node: ET.Element
    ):
        """Write a node in a XML file"""

        # Load tree from node
        tree = ET.ElementTree(node)

        # Make parent directories
        os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

        # Write tree in XML file
        tree.write(
            xml_file_path,
            encoding="utf-8",
            xml_declaration=True
        )
