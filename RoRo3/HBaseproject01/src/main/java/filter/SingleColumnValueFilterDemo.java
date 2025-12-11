package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class SingleColumnValueFilterDemo {
    public static void main(String[] args) throws IOException {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        Table table = connection.getTable(tableName);

        try {
            Scan scan = new Scan();

            // 指定需要扫描的列
            scan.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName"));
            scan.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType"));
            scan.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin"));
            scan.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice"));

            // 创建过滤器：水果类型 = Berries
            SingleColumnValueFilter columnValueFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitType"),  // 修改为 fruitType
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("Berries"))
            );
            columnValueFilter.setFilterIfMissing(true);

            scan.setFilter(columnValueFilter);

            ResultScanner scanner = table.getScanner(scan);

            System.out.println("========== 水果类型为 Berries 的记录 ==========\n");

            for (Result result : scanner) {
                // 获取水果名称
                String fruitName = Bytes.toString(result.getValue(
                        Bytes.toBytes("fruit_info"),
                        Bytes.toBytes("fruitName")
                ));

                // 获取水果产地
                String fruitOrigin = Bytes.toString(result.getValue(
                        Bytes.toBytes("fruit_info"),
                        Bytes.toBytes("fruitOrigin")
                ));

                // 获取销售总额
                String totalPrice = Bytes.toString(result.getValue(
                        Bytes.toBytes("sale_info"),
                        Bytes.toBytes("totalPrice")
                ));

                System.out.println("水果名称: " + fruitName +
                        ", 水果产地: " + fruitOrigin +
                        ", 销售总额: " + totalPrice);
            }
            scanner.close();

        } finally {
            table.close();
            HBaseConnect.closeConnection();
        }
    }
}