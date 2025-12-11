package filter;

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

import connect.HBaseConnect;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 单列值过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 添加完善的异常处理
 * 3. 使用 HBaseUtils 工具类简化代码
 */
public class SingleColumnValueFilterDemo {

    public static void main(String[] args) {
        // 获取连接
        Connection connection = HBaseConnect.getConnection();
        // 获取表名
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建单列值过滤器，4个参数：列族名、列名、比较关系、比较器 返回满足条件的整行数据
            SingleColumnValueFilter columnValueFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitType"),
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("Berries")));
            // 将列值过滤器配置到scan
            scan.setFilter(columnValueFilter);

            // table调用getScanner()查询数据，并遍历打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    // 使用 HBaseUtils 工具类获取数据
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    String fruitOrigin = HBaseUtils.getString(result, "fruit_info", "fruitOrigin");
                    BigDecimal totalPrice = HBaseUtils.getBigDecimal(result, "sale_info", "totalPrice");

                    System.out.print("水果名称:" + fruitName + "\t");
                    System.out.print("水果产地:" + fruitOrigin + "\t");
                    System.out.println("销售总额:" + (totalPrice != null ? totalPrice.toPlainString() : "null"));
                }
            }
        } catch (IOException e) {
            System.err.println("单列值过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}