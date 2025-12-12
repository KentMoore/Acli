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

public class PutDatas {
    private static Connection connection;
    private static Table table;

    public static void main(String[] args) throws IOException {
        connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        table = connection.getTable(tableName);
        String path = "E:\\fruit_info.csv";
        String fruitNo = "";
        String fruitName = "";
        String fruitType = "";
        String fruitOrigin = "";
        BigDecimal unitPrice = null;
        Long quantity = 0L;
        BigDecimal totalPrice = null;

        ArrayList<String[]> csvData = readCsvByCsvReader(path);

        // ============ 修改：puts列表移到循环外部 ============
        ArrayList<Put> puts = new ArrayList<>();

        for (int i = 0; i < csvData.size(); i++) {
            fruitNo = csvData.get(i)[0];
            fruitName = csvData.get(i)[1];
            fruitType = csvData.get(i)[2];
            fruitOrigin = csvData.get(i)[3];
            unitPrice = new BigDecimal(csvData.get(i)[4]);
            quantity = Long.valueOf(csvData.get(i)[5]);
            totalPrice = new BigDecimal(csvData.get(i)[6]);

            Put put = new Put(Bytes.toBytes(fruitNo));

            // ============ 修改：链式调用，不需要多个变量 ============
            put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitName"),
                    Bytes.toBytes(fruitName)
            );
            put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitType"),
                    Bytes.toBytes(fruitType)
            );
            put.addColumn(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitOrigin"),
                    Bytes.toBytes(fruitOrigin)
            );
            // ============ 修改：BigDecimal转String ============
            put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("unitPrice"),
                    Bytes.toBytes(unitPrice.toString())
            );
            // ============ 修改：拼写错误 salr_info -> sale_info ============
            put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("quantity"),
                    Bytes.toBytes(quantity)
            );
            put.addColumn(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("totalPrice"),
                    Bytes.toBytes(totalPrice.toString())
            );

            // ============ 补充：将put添加到列表 ============
            puts.add(put);
        }

        // ============ 补充：批量插入数据 ============
        table.put(puts);

        // ============ 补充：关闭资源 ============
        table.close();
        connection.close();

        System.out.println("数据导入完成！共导入 " + puts.size() + " 条记录");
    }

    private static ArrayList<String[]> readCsvByCsvReader(String path) {
        ArrayList<String[]> arrayList = new ArrayList<String[]>();
        try {
            CsvReader csvReader = new CsvReader(
                    path,
                    ',',
                    Charset.forName("UTF-8")
            );
            while (csvReader.readRecord()) {
                arrayList.add(csvReader.getValues());
            }
            csvReader.close();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return arrayList;
    }
}