package filter;

import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.QualifierFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;

import java.io.IOException;

/**
 * 列限定符过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 移除未使用的静态变量和 import
 * 3. 添加完善的异常处理
 */
public class QualifierFilterDemo {

    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建列限定符过滤器，2个参数：比较关系和比较器，返回：满足条件的列数据
            QualifierFilter qualifierFilter = new QualifierFilter(
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("quantity")));
            // 将过滤器配置到Scan对象中
            scan.setFilter(qualifierFilter);

            // table调用getScanner()方法查询数据，遍历并打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    // 获取水果销量quantity的值
                    byte[] quantityBytes = result.getValue(Bytes.toBytes("sale_info"), Bytes.toBytes("quantity"));
                    Long quantity = quantityBytes != null ? Bytes.toLong(quantityBytes) : null;
                    // 获取rowKey（水果编号）的值
                    String rowKey = Bytes.toString(result.getRow());
                    System.out.println("水果编号：" + rowKey + ",销量：" + quantity);
                }
            }
        } catch (IOException e) {
            System.err.println("列限定符过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}