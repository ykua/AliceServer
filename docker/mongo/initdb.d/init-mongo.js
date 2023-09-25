db = db.getSiblingDB('alice');  // aliceデータベースを参照
// daqコレクションが存在しない場合のみ作成
if (!db.getCollectionNames().includes('daq')) {
    db.createCollection('daq');
}

// 初期データコレクションのインサート
db.daq.insertMany([
    {
        node_number: "test-001",
        data_type: "temperature",
        data_category: "sensor",
        daq_value: 0.1,
        date: ISODate("2023-09-23T00:00:00Z"),
    },
    {
        node_number: "test-001",
        data_type: "temperature",
        data_category: "sensor",
        daq_value: 0.25,
        date: ISODate("2023-09-23T00:00:01Z"),
    },
]);