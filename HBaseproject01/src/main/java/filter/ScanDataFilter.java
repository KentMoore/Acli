package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 使用过滤器扫描数据示例
 * 
 * 优化点：
 * 1. 使用 HBaseUtils 工具类替代重复定义的方法
 * 2. 使用 try-with-resources 自动关闭所有资源
 */
public class ScanDataFilter {

    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = conn.getTable(tableName)) {
            // 构造 Scan
            Scan scan = new Scan();
            scan.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName"));
            scan.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice"));
            scan.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice"));
            scan.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("quantity"));

            // 单列值过滤器：sale_info:quantity <= 200
            SingleColumnValueFilter filter = new SingleColumnValueFilter(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("quantity"),
                    CompareOperator.LESS_OR_EQUAL,
                    new BinaryComparator(Bytes.toBytes(200L)));
            filter.setFilterIfMissing(true);
            scan.setFilter(filter);

            // 扫描并输出结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                System.out.println("fruitName\tunitPrice\ttotalPrice");
                for (Result result : scanner) {
                    // 使用 HBaseUtils 工具类
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    BigDecimal unitPrice = HBaseUtils.getBigDecimal(result, "sale_info", "unitPrice");
                    BigDecimal totalPrice = HBaseUtils.getBigDecimal(result, "sale_info", "totalPrice");

                    System.out.println(
                            fruitName + "\t" +
                                    (unitPrice == null ? "null" : unitPrice.toPlainString()) + "\t" +
                                    (totalPrice == null ? "null" : totalPrice.toPlainString()));
                }
            }
        } catch (IOException e) {
            System.err.println("过滤扫描失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
