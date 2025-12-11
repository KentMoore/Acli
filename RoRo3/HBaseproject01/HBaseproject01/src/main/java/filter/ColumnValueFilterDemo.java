package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.List;

public class ColumnValueFilterDemo {
    public static void main(String[] args) throws IOException {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        Table table = connection.getTable(tableName);

        Scan scan = new Scan();

        // 先扫描所有数据，在代码中过滤
        for (Result result : table.getScanner(scan)) {
            List<Cell> cellList = result.listCells();

            String rowKey = Bytes.toString(result.getRow());

            // 获取 totalPrice 列的值
            byte[] totalPriceBytes = result.getValue(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("totalPrice")
            );

            if (totalPriceBytes != null) {
                String totalPriceStr = Bytes.toString(totalPriceBytes);
                double totalPrice = Double.parseDouble(totalPriceStr);

                // 在代码中进行数值比较：小于等于200
                if (totalPrice <= 200) {
                    System.out.println("水果编号：" + rowKey + "，销售总额为：" + totalPrice);
                }
            }
        }

        table.close();
        HBaseConnect.closeConnection();
    }
}