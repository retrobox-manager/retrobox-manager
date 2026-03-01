#!/usr/bin/python3
"""XML Helper"""

import xml.etree.ElementTree as ET

from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class XmlHelper:
    """Class to help usage of XML"""

    @staticmethod
    def __matches_criteria(node: ET.Element, criteria: dict[str, str]) -> bool:
        """Check if node matches all criteria"""
        for field, expected in criteria.items():
            field_node = node.find(field)
            if field_node is None or not field_node.text.endswith(expected):
                return False
        return True

    @staticmethod
    def __cast_value(value: str) -> any:
        """Cast a value"""

        value = value.strip()
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if value.isdigit():
            return int(value)
        return value

    @staticmethod
    def __to_text(value) -> str:
        """Transform value to Text"""

        if isinstance(value, bool):
            return "True" if value else "False"
        return str(value)

    @staticmethod
    def __singular(tag: str) -> str:
        """Retrieve tag to singular"""

        if tag.endswith("ies"):
            return tag[:-3] + "y"
        if tag.endswith("s"):
            return tag[:-1]
        return tag

    @staticmethod
    def __indent(elem, level=0):
        """Indent XML"""

        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "

            for child in elem:
                XmlHelper.__indent(child, level + 1)

            last = elem[-1]
            if not last.tail or not last.tail.strip():
                last.tail = i

        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

    @staticmethod
    def __xml_to_obj(elem: ET.Element) -> any:
        """Transform XML to Object"""

        children = list(elem)

        if not children and not elem.attrib:
            return XmlHelper.__cast_value((elem.text or "").strip())

        obj = {}
        if elem.attrib:
            obj["@attr"] = {k: XmlHelper.__cast_value(v)
                            for k, v in elem.attrib.items()}

        groups = {}
        for child in children:
            groups.setdefault(child.tag, []).append(
                XmlHelper.__xml_to_obj(child))

        result = {}
        for tag, values in groups.items():
            if XmlHelper.__singular(elem.tag) == tag:
                result = values if len(values) > 1 else values
            else:
                result[tag] = values[0] if len(values) == 1 else values

        if obj:
            if isinstance(result, dict):
                obj.update(result)
            else:
                return obj, result
            return obj

        return result

    @staticmethod
    def __obj_to_xml(tag: str, obj: any) -> ET.Element:
        """Transform Object to XML"""

        elem = ET.Element(tag)

        if not isinstance(obj, (dict, list)):
            elem.text = XmlHelper.__to_text(obj)
            return elem

        if isinstance(obj, list):
            item_tag = XmlHelper.__singular(tag)
            for item in obj:
                elem.append(XmlHelper.__obj_to_xml(item_tag, item))
            return elem

        for key, value in obj.items():
            if key == "@attr":
                for attr, attr_value in value.items():
                    elem.set(attr, XmlHelper.__to_text(attr_value))

            elif isinstance(value, list):
                elem.append(XmlHelper.__obj_to_xml(key, value))

            else:
                elem.append(XmlHelper.__obj_to_xml(key, value))

        if len(elem) == 0 and elem.text is None:
            elem.text = ""

        return elem

    @staticmethod
    def load_xml(
        xml_file_path: str
    ) -> any:
        """Load XML file"""

        # Do nothing if XML file doesn't exist
        if not FileHelper.is_file_exists(xml_file_path):
            return None

        tree = ET.parse(xml_file_path)
        return XmlHelper.__xml_to_obj(tree.getroot())

    @staticmethod
    def save_xml(
        xml_file_path: str,
        root_tag: str,
        obj: any,
        force: bool = False
    ) -> bool:
        """Save XML file"""

        # Do nothing if simulation
        if Context.is_simulated() and not force:
            return False

        root = XmlHelper.__obj_to_xml(root_tag, obj)
        tree = ET.ElementTree(root)
        XmlHelper.__indent(root)
        tree.write(
            xml_file_path,
            encoding="utf-8",
            xml_declaration=True
        )
        return True

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
                if XmlHelper.__matches_criteria(node, criteria):
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
                if XmlHelper.__matches_criteria(node, criteria):
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

        # Do nothing if simulation
        if Context.is_simulated():
            return False

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
                if XmlHelper.__matches_criteria(node, criteria):
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
