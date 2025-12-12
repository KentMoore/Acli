package filter;

import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.FamilyFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;
import util.HBaseUtils;

import java.io.IOException;

/**
 * 列族过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 移除未使用的静态变量
 * 3. 添加完善的异常处理
 * 4. 使用 HBaseUtils 工具类简化代码
 */
public class FamilyFilterDemo {

    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建列族过滤器,2参数：比较关系、比较器，返回：满足条件的行数据
            FamilyFilter familyFilter = new FamilyFilter(
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("fruit_info")));
            // 将过滤器配置到scan对象
            scan.setFilter(familyFilter);

            // table调用getScanner()查询数据，并遍历打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    String fruitOrigin = HBaseUtils.getString(result, "fruit_info", "fruitOrigin");
                    String fruitType = HBaseUtils.getString(result, "fruit_info", "fruitType");
                    System.out.println("水果名称：" + fruitName + "，水果类型：" + fruitType + ",水果产地：" + fruitOrigin);
                }
            }
        } catch (IOException e) {
            System.err.println("列族过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}