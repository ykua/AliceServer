db = db.getSiblingDB('alice');  // aliceデータベースを参照
// daqコレクションが存在しない場合のみ作成
if (!db.getCollecitonNames().includes('daq')) {
    db.createCollection('daq');
}

// 初期データコレクションのインサート
db.daq.insertMany([
    {name: "data1", value: "sample1"},
    {name: "data2", value: "sample2"},
]);