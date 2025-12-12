package data;

import com.csvreader.CsvReader;

import connect.HBaseConnect;

import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.Charset;
import java.util.ArrayList;

public class PutDatas4 {
    private static Connection conn;
    private static Table table;

    public static void main(String[] args) throws IOException {
        // 连接
        conn = HBaseConnect.getConnection();
        // 获取表
        TableName tableName = TableName.valueOf("commodity:fruit_table");
        table = conn.getTable(tableName);
        String fruitNo = "";
        String fruitName = "";
        String fruitType = "";
        String fruitOringin = "";
        BigDecimal unitPrice = null;
        Long quantity = 0L;
        BigDecimal totalPrice = null;
        String path = "E:\\fruit_info.csv";
        ArrayList<String[]> csvData = readCsvByCsvReader(path);
        // csvData中的第一个值：fruit001,Banana,Tropical and subtropical
        // fruits,Yunnan,5.5,157,863.5
        for (int i = 0; i < csvData.size(); i++) {
            fruitNo = csvData.get(i)[0];
            fruitName = csvData.get(i)[1];
            fruitType = csvData.get(i)[2];
            fruitOringin = csvData.get(i)[3];
            unitPrice = new BigDecimal(csvData.get(i)[4]);
            quantity = Long.valueOf(csvData.get(i)[5]);
            totalPrice = new BigDecimal(csvData.get(i)[6]);
            ArrayList<Put> puts = new ArrayList<>();
            Put put = new Put(Bytes.toBytes(fruitNo));
            Put put1 = put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitName"),
                    Bytes.toBytes(fruitName));
            Put put2 = put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitType"),
                    Bytes.toBytes(fruitType));
            Put put3 = put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitOrigin"),
                    Bytes.toBytes(fruitOringin));
            Put put4 = put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("unitPrice"),
                    Bytes.toBytes(unitPrice));
            Put put5 = put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("quantity"),
                    Bytes.toBytes(quantity));
            Put put6 = put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("totalPrice"),
                    Bytes.toBytes(totalPrice));
            puts.add(put1);
            puts.add(put2);
            puts.add(put3);
            puts.add(put4);
            puts.add(put5);
            puts.add(put6);
            table.put(puts);
        }
        HBaseConnect.closeConnection();
    }

    private static ArrayList<String[]> readCsvByCsvReader(String path) {
        ArrayList<String[]> arrList = new ArrayList<String[]>();
        try {
            // 将csv源文件的数据读取到CsvReader中
            CsvReader csvReader = new CsvReader(
                    path,
                    ',',
                    Charset.forName("UTF-8"));
            // 从CsvReader中将数据填入数组中
            while (csvReader.readRecord()) {
                arrList.add(csvReader.getValues());
            }
            csvReader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return arrList;
    }
}
