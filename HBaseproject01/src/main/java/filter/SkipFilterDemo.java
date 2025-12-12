package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.SkipFilter;
import org.apache.hadoop.hbase.filter.ValueFilter;
import org.apache.hadoop.hbase.filter.WhileMatchFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.List;

public class SkipFilterDemo {
    public static void main(String[] args) throws IOException {
        // 获取连接
        Connection connection = HBaseConnect.getConnection();
        // 获取表对象
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        Table table = connection.getTable(tableName);
        // 创建Scan对象
        Scan scan = new Scan();
        // 创建值过滤器
        ValueFilter valueFilter = new ValueFilter(
                CompareOperator.NOT_EQUAL,
                new BinaryComparator(Bytes.toBytes("Berries")));
        // 创建跳转过滤器
        SkipFilter skipFilter = new SkipFilter(valueFilter);
        // 创建全匹配过滤器
        WhileMatchFilter whileMatchFilter = new WhileMatchFilter(valueFilter);
        // 将过滤器配置到scan对象中
        scan.setFilter(whileMatchFilter);
        // table调用getScanner()方法查询数据，遍历打印查询结果
        for (Result result : table.getScanner(scan)) {
            List<Cell> cellList = result.listCells();
            Object value = null;
            for (Cell cell : cellList) {
                String rowKey = new String(
                        cell.getRowArray(),
                        cell.getRowOffset(),
                        cell.getRowLength());
                String family = new String(
                        cell.getFamilyArray(),
                        cell.getFamilyOffset(),
                        cell.getFamilyLength());
                String qualifier = new String(
                        cell.getQualifierArray(),
                        cell.getQualifierOffset(),
                        cell.getQualifierLength());
                if (qualifier.equals("unitPrice") || qualifier.equals("quantity") || qualifier.equals("totalPrice")) {
                    value = Bytes.toBigDecimal(
                            cell.getValueArray(),
                            cell.getValueOffset(),
                            cell.getValueLength());
                } else {
                    value = new String(
                            cell.getValueArray(),
                            cell.getValueOffset(),
                            cell.getValueLength());
                }
                System.out.println("水果编号：" + rowKey + "\t列族：" + family + "\t列名：" + qualifier + "\t值：" + value);
            }
        }
        HBaseConnect.closeConnection();
    }
}