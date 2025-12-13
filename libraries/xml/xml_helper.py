#!/usr/bin/python3
"""XML Helper"""

import xml.etree.ElementTree as ET

from libraries.file.file_helper import FileHelper


class XmlHelper:
    """Class to help usage of XML"""

    @staticmethod
    def _matches_criteria(node: ET.Element, criteria: dict[str, str]) -> bool:
        """Check if node matches all criteria"""
        for field, expected in criteria.items():
            field_node = node.find(field)
            if field_node is None or field_node.text != expected:
                return False
        return True

    @staticmethod
    def print_all_tags(
        xml_file_path: str
    ):
        """Show content"""

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Print all tags
        for elem in root.iter():
            print(f"Tag : {elem.tag}  |  Text : {elem.text!r}")

    @staticmethod
    def list_tag_values(
        xml_file_path: str,
        parent_tag: str,
        tag: str
    ) -> list[str]:
        """List values for a tag from a XML file"""

        # Initialize result
        result = []

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return result

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Retrieve parents
        if parent_tag == root.tag:
            parents = [root]
        else:
            parents = root.findall(f'.//{parent_tag}')

        # For each parent
        for parent in parents:
            # For each parent's node
            for node in list(parent):
                # If bad tag, continue
                if node.tag != tag:
                    continue

                # Add node's text
                result.append(node.text)

        return result

    @staticmethod
    def get_tag_data(
        xml_file_path: str,
        parent_tag: str,
        tag: str,
        criteria: dict[str, str]
    ) -> list[dict[str, str]]:
        """Return the data dict for the first tag matching the criteria"""

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return {}

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Retrieve parents
        if parent_tag == root.tag:
            parents = [root]
        else:
            parents = root.findall(f'.//{parent_tag}')

        # For each parent
        for parent in parents:
            # For each parent's node
            for node in list(parent):
                # If bad tag, continue
                if node.tag != tag:
                    continue

                # If matches criteria, return dict of all fields
                if XmlHelper._matches_criteria(node, criteria):
                    return {child.tag: child.text for child in node}

        # No match
        return {}

    @staticmethod
    def get_tag_content(
        xml_file_path: str,
        parent_tag: str,
        tag: str,
        criteria: dict[str, str]
    ) -> str:
        """Return the content for the first tag matching the criteria"""

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return None

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Retrieve parents
        if parent_tag == root.tag:
            parents = [root]
        else:
            parents = root.findall(f'.//{parent_tag}')

        # For each parent
        for parent in parents:
            # For each parent's node
            for node in list(parent):
                # If bad tag, continue
                if node.tag != tag:
                    continue

                # If matches criteria, return content of all fields
                if XmlHelper._matches_criteria(node, criteria):
                    return ET.tostring(node, encoding="unicode")

        # No match
        return None

    @staticmethod
    def delete_tag(
        xml_file_path: str,
        parent_tag: str,
        tag: str,
        criteria: dict[str, str]
    ) -> bool:
        """Delete the first tag matching the criteria"""

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return False

        # Load tree from XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Retrieve parents
        if parent_tag == root.tag:
            parents = [root]
        else:
            parents = root.findall(f'.//{parent_tag}')

        # For each parent
        for parent in parents:
            # For each parent's node
            for node in list(parent):
                # If bad tag, continue
                if node.tag != tag:
                    continue

                # If matches criteria, delete the tag in XML file
                if XmlHelper._matches_criteria(node, criteria):
                    node.tail = None
                    parent.remove(node)
                    ET.indent(tree, space="  ")
                    tree.write(
                        xml_file_path,
                        encoding="utf-8",
                        xml_declaration=True
                    )
                    return True

        # No match
        return False
