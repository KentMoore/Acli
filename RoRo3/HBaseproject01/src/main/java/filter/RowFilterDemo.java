package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.RowFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;

public class RowFilterDemo {
    static Connection connection;
    static Table table;

    public static void main(String[] args) throws IOException {
        connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        table = connection.getTable(tableName);

        Scan scan = new Scan();
        RowFilter rowFilter = new RowFilter(
                CompareOperator.GREATER,
                new BinaryComparator(Bytes.toBytes("fruit009"))
        );
        scan.setFilter(rowFilter);

        for (Result result : table.getScanner(scan)) {
            // 获取Rowkey
            String rowkey = Bytes.toString(result.getRow());

            // 获取水果信息（字符串）
            String fruitName = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName")));
            String fruitType = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType")));
            String fruitOrigin = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin")));

            // ====== 关键修改 ======
            // unitPrice: 写入是String，读取也用String，再转BigDecimal
            String unitPriceStr = Bytes.toString(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice")));
            BigDecimal unitPrice = new BigDecimal(unitPriceStr);

            // quantity: 写入是Long，读取也用Long ✓
            Long quantity = Bytes.toLong(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("quantity")));

            // totalPrice: 写入是String，读取也用String，再转BigDecimal
            String totalPriceStr = Bytes.toString(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice")));
            BigDecimal totalPrice = new BigDecimal(totalPriceStr);

            System.out.println("水果编号:" + rowkey +
                    "，水果名:" + fruitName +
                    "，水果类型:" + fruitType +
                    "，水果产地:" + fruitOrigin +
                    "，单价：" + unitPrice +
                    "，销量：" + quantity +
                    "，销售额：" + totalPrice);
        }

        table.close();
        HBaseConnect.closeConnection();
    }
}