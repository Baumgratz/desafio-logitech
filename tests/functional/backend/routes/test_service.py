import pytest

from backend.models import Item, Truck

ANY_NAME = "ANY_NAME"
ANY_WEIGHT = 123.456


@pytest.fixture
def mock_truck_list(client, test_db, truck_list):
    truck_list = []
    for truck in truck_list:
        with test_db as db:
            db_truck = Truck(name=truck["name"], weight_max=truck["weight_max"])
            db.add(db_truck)
            db.commit()
            db.refresh(db_truck)
            truck_list.append(db_truck)
    return truck_list


@pytest.fixture
def mock_item_list(client, test_db, item_list):
    item_list = []
    for item in item_list:
        with test_db as db:
            db_item = Item(name=item["name"], weight=item["weight"])
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            item_list.append(db_item)
    return item_list


@pytest.mark.parametrize(
    "item_list, truck_list, expected_truck_item_relation",
    [
        (
            [
                {"name": "Caixa de ferramenta", "weight": 2},  # 1
                {"name": "Motor Peças", "weight": 3},  # 2
                {"name": "Bobina de cobre", "weight": 2.5},  # 3
                {"name": "Palete de Madeira", "weight": 2.5},  # 4
                {"name": "Compressor de Ar", "weight": 5},  # 5
                {"name": "Tanque de Óleo", "weight": 3},  # 6
                {"name": "Barril de Produtos", "weight": 2},  # 7
                {"name": "Geração de Energia", "weight": 2.5},  # 8
                {"name": "Conjunto de Rodas", "weight": 1.5},  # 9
                {"name": "Painel Solar", "weight": 1},  # 10
            ],
            [
                {"name": "Truck Azul", "weight_max": 10},  # 1
                {"name": "Truck Vermelho", "weight_max": 15},  # 2
            ],
            (
                (1, 1),
                (2, 1),
                (3, 2),
                (4, 2),
                (5, 1),
                (6, 2),
                (7, 2),
                (8, 2),
                (9, 2),
                (10, 2),
            ),
        )
    ],
)
def test_service_distribuir(
    client, test_db, item_list, truck_list, expected_truck_item_relation
):
    response = client.get("/distribuir")

    return response.json()["mensagem"] == "Distribuição realizada"

    for item_id, truck_id in expected_truck_item_relation:
        with test_db as db:

            item = db.query(Item).filter(Truck.id == truck_id).first()
            assert item.truck_id == truck_id
