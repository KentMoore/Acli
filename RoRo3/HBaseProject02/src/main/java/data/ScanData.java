package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 扫描数据示例
 * 
 * 优化点：
 * 1. 使用 HBaseUtils 工具类替代重复定义的方法
 * 2. 使用 try-with-resources 自动关闭资源
 */
public class ScanData {

    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = conn.getTable(tableName)) {
            // 构造 Scan
            Scan scan = new Scan();
            scan.addFamily(Bytes.toBytes("fruit_info"));
            scan.addFamily(Bytes.toBytes("sale_info"));

            try (ResultScanner scanner = table.getScanner(scan)) {
                System.out.println("=== Scan Result from commodity1:fruit_table ===");

                for (Result result : scanner) {
                    String rowKey = Bytes.toString(result.getRow());

                    // 使用 HBaseUtils 工具类
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    String fruitType = HBaseUtils.getString(result, "fruit_info", "fruitType");
                    String fruitOrigin = HBaseUtils.getString(result, "fruit_info", "fruitOrigin");

                    BigDecimal unitPrice = HBaseUtils.getBigDecimal(result, "sale_info", "unitPrice");
                    Long quantity = HBaseUtils.getLong(result, "sale_info", "quantity");
                    BigDecimal totalPrice = HBaseUtils.getBigDecimal(result, "sale_info", "totalPrice");

                    System.out.println("----------------------------------------------");
                    System.out.println("RowKey      : " + rowKey);
                    System.out.println("fruitName   : " + fruitName);
                    System.out.println("fruitType   : " + fruitType);
                    System.out.println("fruitOrigin : " + fruitOrigin);
                    System.out.println("unitPrice   : " + (unitPrice == null ? "null" : unitPrice.toPlainString()));
                    System.out.println("quantity    : " + (quantity == null ? "null" : quantity));
                    System.out.println("totalPrice  : " + (totalPrice == null ? "null" : totalPrice.toPlainString()));
                }

                System.out.println("=== Scan Finished ===");
            }
        } catch (IOException e) {
            System.err.println("扫描数据失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
