package filter;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.ValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;

import java.io.IOException;
import java.util.List;

/**
 * 值过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 添加完善的异常处理
 */
public class ValueFilterDemo {

    public static void main(String[] args) {
        // 获取连接
        Connection connection = HBaseConnect.getConnection();
        // 获取表名
        TableName tableName = TableName.valueOf("commodity:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建值过滤器
            ValueFilter valueFilter = new ValueFilter(
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("Hainan")));
            // 将值过滤器配置到scan中
            scan.setFilter(valueFilter);

            // 调用getScanner查询数据并遍历打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    List<Cell> cellList = result.listCells();
                    for (Cell cell : cellList) {
                        String rowKey = new String(
                                cell.getRowArray(),
                                cell.getRowOffset(),
                                cell.getRowLength());
                        System.out.println("水果编号：" + rowKey);
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("值过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}