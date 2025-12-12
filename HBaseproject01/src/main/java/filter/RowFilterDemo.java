package filter;

import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.RowFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 行过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 移除未使用的静态变量
 * 3. 添加完善的异常处理
 * 4. 使用 HBaseUtils 工具类简化代码
 */
public class RowFilterDemo {

    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建行过滤器RowFilter，2个参数：比较关系和比较器，返回：满足条件的具体行数据
            RowFilter rowFilter = new RowFilter(
                    CompareOperator.LESS_OR_EQUAL,
                    new BinaryComparator(Bytes.toBytes("fruit002")));
            // 将行过滤器配置到Scan对象中
            scan.setFilter(rowFilter);

            // table调用getScanner()方法查询数据，遍历并打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    // 使用 HBaseUtils 工具类获取数据
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    String fruitType = HBaseUtils.getString(result, "fruit_info", "fruitType");
                    String fruitOrigin = HBaseUtils.getString(result, "fruit_info", "fruitOrigin");
                    BigDecimal unitPrice = HBaseUtils.getBigDecimal(result, "sale_info", "unitPrice");
                    Long quantity = HBaseUtils.getLong(result, "sale_info", "quantity");
                    BigDecimal totalPrice = HBaseUtils.getBigDecimal(result, "sale_info", "totalPrice");
                    String rowKey = Bytes.toString(result.getRow());

                    System.out.println("水果编号：" + rowKey + ",水果名：" + fruitName + ",水果类型：" + fruitType +
                            "，水果产地：" + fruitOrigin + ",单价：" + unitPrice + ",销量：" + quantity + ",销售额：" + totalPrice);
                }
            }
        } catch (IOException e) {
            System.err.println("行过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}