#!/usr/bin/python3
"""XML Helper"""

import os
from typing import Dict, List
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
        parent_tag: str | None = None
    ) -> List[str]:
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
                found_tag = node.find(tag)
                if found_tag is not None:
                    result.append(found_tag.text)

        return result

    @staticmethod
    def list_tag_data(
        xml_file_path: str,
        tag: str,
        parent_tag: str | None = None
    ) -> List[Dict[str, str]]:
        """List data for a tag from a XML file"""

        # Initialize result
        result = []

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # List values for the specified tag
        if parent_tag is None:
            for node in root.iter(tag):
                result.append(
                    {child.tag: child.text for child in node}
                )
        else:
            for node in root.findall(f'.//{parent_tag}'):
                found_tag = node.find(tag)
                if found_tag is not None:
                    result.append(
                        {child.tag: child.text for child in found_tag}
                    )

        return result

    @staticmethod
    def get_tag_data(
        xml_file_path: str,
        tag: str,
        criteria: Dict[str, str],
        parent_tag: str | None = None
    ) -> List[Dict[str, str]]:
        """Return the data dict for the first tag matching the criteria"""

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Select nodes depending on parent_tag
        if parent_tag is None:
            nodes = root.iter(tag)
        else:
            nodes = []
            for node in root.findall(f'.//{parent_tag}'):
                found_tag = node.find(tag)
                if found_tag is not None:
                    nodes.append(found_tag)

        # Search for a node matching all criteria
        for node in nodes:
            is_match = True
            for field, expected in criteria.items():
                field_node = node.find(field)
                if field_node is None or field_node.text != expected:
                    is_match = False
                    break

            if is_match:
                # Return dict of all fields
                return {child.tag: child.text for child in node}

        # No match
        return {}

    @staticmethod
    def get_tag_content(
        xml_file_path: str,
        tag: str,
        criteria: Dict[str, str],
        parent_tag: str | None = None
    ) -> str:
        """Return the content for the first tag matching the criteria"""

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Select nodes depending on parent_tag
        if parent_tag is None:
            nodes = root.iter(tag)
        else:
            nodes = []
            for node in root.findall(f'.//{parent_tag}'):
                found_tag = node.find(tag)
                if found_tag is not None:
                    nodes.append(found_tag)

        # Search for a node matching all criteria
        for node in nodes:
            is_match = True
            for field, expected in criteria.items():
                field_node = node.find(field)
                if field_node is None or field_node.text != expected:
                    is_match = False
                    break

            if is_match:
                # Return dict of all fields
                return ET.tostring(node, encoding="unicode")

        # No match
        return None

    @staticmethod
    def create_xml_from_list(
        xml_file_path: str,
        data: List[Dict[str, str]],
        root_tag: str,
        item_tag: str,
    ):
        """Generate an XML from a list of dictionaries"""

        root = ET.Element(root_tag)

        for item_dict in data:
            item_element = ET.SubElement(root, item_tag)

            for key, value in item_dict.items():
                child = ET.SubElement(item_element, key)
                child.text = value

        # Good indentation
        ET.indent(root, space="    ")

        # Load tree from node
        tree = ET.ElementTree(root)

        # Make parent directories
        os.makedirs(
            os.path.dirname(xml_file_path),
            exist_ok=True
        )

        # Write tree in XML file
        tree.write(
            xml_file_path,
            encoding="utf-8",
            xml_declaration=True
        )

    # @staticmethod
    # def write_node(
    #     xml_file_path: str,
    #     node: ET.Element
    # ):
    #     """Write a node in a XML file"""

    #     # Load tree from node
    #     tree = ET.ElementTree(node)

    #     # Make parent directories
    #     os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

    #     # Write tree in XML file
    #     tree.write(
    #         xml_file_path,
    #         encoding="utf-8",
    #         xml_declaration=True
    #     )
