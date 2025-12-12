package filter;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BigDecimalComparator;
import org.apache.hadoop.hbase.filter.ColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.List;

/**
 * 列值过滤器示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Table 和 ResultScanner 资源
 * 2. 添加完善的异常处理
 */
public class ColumnValueFilterDemo {

    public static void main(String[] args) {
        // 获取连接
        Connection connection = HBaseConnect.getConnection();
        // 获取表名
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            // 创建Scan对象
            Scan scan = new Scan();
            // 创建列值过滤器，4个参数：列族名、列名、比较关系、比较器 返回满足条件的单元格
            ColumnValueFilter columnValueFilter = new ColumnValueFilter(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("totalPrice"),
                    CompareOperator.GREATER_OR_EQUAL,
                    new BigDecimalComparator(BigDecimal.valueOf(5000)));
            // 将列值过滤器配置到scan
            scan.setFilter(columnValueFilter);

            // table调用getScanner()查询数据，并遍历打印结果
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    List<Cell> cellList = result.listCells();
                    for (Cell cell : cellList) {
                        // 获取rowkey
                        String rowKey = new String(
                                cell.getRowArray(),
                                cell.getRowOffset(),
                                cell.getRowLength());
                        // 获取单元格的值：totalPrice的值
                        BigDecimal value = Bytes.toBigDecimal(
                                cell.getValueArray(),
                                cell.getValueOffset(),
                                cell.getValueLength());
                        System.out.println("水果编号：" + rowKey + "，销售总额为：" + value);
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("列值过滤查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}