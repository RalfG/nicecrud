# from rich import print
import pytest
from pydantic import BaseModel, Field

from frontend.basemodel_to_table import (basemodel_to_columns,
                                         basemodellist_to_rows,
                                         basemodellist_to_rows_and_cols)
from objectmvp.model import Model
from objectmvp.source import Source


def test_basemodellist():
    yolo_world = Model(
        cvmodel_id="yolo_world",
        file="models/cups.pt",
        typ="YOLO",
        objects=["drone", "cloud"],
    )
    camera = Source(
        source_id="camera2",
        typ="video_file",
        url="./doesnotexist.mp4",
        models={yolo_world.cvmodel_id: yolo_world},
    )
    birk = Source(
        source_id="camera3",
        typ="video_file",
        url="./doesnotexist.mp4",
        models={yolo_world.cvmodel_id: yolo_world},
    )
    basemodellist = [camera, birk]
    r, c = basemodellist_to_rows_and_cols(basemodellist)
    assert "source_id" in [x["name"] for x in c]
    assert "camera3" in [x["source_id"] for x in r]


class Bicycle(BaseModel):
    brand: str = Field(..., title="Brand")
    model: str = Field(..., title="Model")
    gear_count: int = Field(..., title="Gear Count")
    is_electric: bool = Field(False, title="Is Electric")


@pytest.fixture
def bicycle_list():
    return [
        Bicycle(brand="Trek", model="Marlin 7", gear_count=21, is_electric=False),
        Bicycle(brand="Cannondale", model="Trail 6", gear_count=18, is_electric=False),
        Bicycle(brand="Specialized", model="Turbo Levo", gear_count=11, is_electric=True),
    ]


def test_basemodel_to_columns():
    expected_columns = [
        {"name": "brand", "label": "Brand", "field": "brand"},
        {"name": "model", "label": "Model", "field": "model"},
        {"name": "gear_count", "label": "Gear Count", "field": "gear_count"},
        {"name": "is_electric", "label": "Is Electric", "field": "is_electric"},
    ]
    assert basemodel_to_columns(Bicycle) == expected_columns


def test_basemodel_to_columns_with_exclude(bicycle_list):
    exclude_fields = {"is_electric"}
    expected_columns = [
        {"name": "brand", "label": "Brand", "field": "brand"},
        {"name": "model", "label": "Model", "field": "model"},
        {"name": "gear_count", "label": "Gear Count", "field": "gear_count"},
    ]
    assert basemodel_to_columns(Bicycle, exclude=exclude_fields) == expected_columns


def test_basemodel_to_columns_with_include(bicycle_list):
    include_fields = {"brand", "model"}
    expected_columns = [
        {"name": "brand", "label": "Brand", "field": "brand"},
        {"name": "model", "label": "Model", "field": "model"},
    ]
    assert basemodel_to_columns(Bicycle, include=include_fields) == expected_columns


def test_basemodellist_to_rows(bicycle_list):
    expected_rows = [
        {"brand": "Trek", "model": "Marlin 7", "gear_count": 21, "is_electric": False},
        {"brand": "Cannondale", "model": "Trail 6", "gear_count": 18, "is_electric": False},
        {"brand": "Specialized", "model": "Turbo Levo", "gear_count": 11, "is_electric": True},
    ]
    assert basemodellist_to_rows(bicycle_list) == expected_rows


def test_basemodellist_to_rows_and_cols(bicycle_list):
    expected_columns = [
        {"name": "brand", "label": "Brand", "field": "brand"},
        {"name": "model", "label": "Model", "field": "model"},
        {"name": "gear_count", "label": "Gear Count", "field": "gear_count"},
        {"name": "is_electric", "label": "Is Electric", "field": "is_electric"},
    ]
    expected_rows = [
        {"brand": "Trek", "model": "Marlin 7", "gear_count": 21, "is_electric": False},
        {"brand": "Cannondale", "model": "Trail 6", "gear_count": 18, "is_electric": False},
        {"brand": "Specialized", "model": "Turbo Levo", "gear_count": 11, "is_electric": True},
    ]

    rows, columns = basemodellist_to_rows_and_cols(bicycle_list)
    assert columns == expected_columns
    assert rows == expected_rows
