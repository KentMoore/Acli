package filter;

import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BigDecimalComparator;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.FilterList;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 高销售额或云南产地过滤器
 * 
 * 查询条件（满足任意一个即可）：
 * 1. 销售额（totalPrice）> 2000
 * 2. 产地（fruitOrigin）= Yunnan
 */
public class HighSalesOrYunnanOriginFilter {

    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();
        System.out.println("HBase 连接已创建");
        
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            Scan scan = new Scan();
            
            // 创建过滤器列表（使用 OR 逻辑）
            FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ONE);
            
            // 过滤器1：销售额 > 2000
            SingleColumnValueFilter totalPriceFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("totalPrice"),
                    CompareOperator.GREATER,
                    new BigDecimalComparator(BigDecimal.valueOf(2000)));
            
            // 过滤器2：产地 = Yunnan
            SingleColumnValueFilter originFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("fruit_info"),
                    Bytes.toBytes("fruitOrigin"),
                    CompareOperator.EQUAL,
                    new BinaryComparator(Bytes.toBytes("Yunnan")));
            
            // 将两个过滤器添加到过滤器列表
            filterList.addFilter(totalPriceFilter);
            filterList.addFilter(originFilter);
            
            // 配置过滤器到 scan
            scan.setFilter(filterList);

            System.out.println("=== 查询结果：销售额 > 2000 或 产地 = Yunnan ===");
            System.out.println("RowKey\tfruitName\tfruitType\tfruitOrigin\tunitPrice\tquantity\ttotalPrice");
            System.out.println("----------------------------------------------");
            
            try (ResultScanner scanner = table.getScanner(scan)) {
                int count = 0;
                for (Result result : scanner) {
                    count++;
                    // 获取水果信息
                    String rowKey = Bytes.toString(result.getRow());
                    String fruitName = HBaseUtils.getString(result, "fruit_info", "fruitName");
                    String fruitType = HBaseUtils.getString(result, "fruit_info", "fruitType");
                    String fruitOrigin = HBaseUtils.getString(result, "fruit_info", "fruitOrigin");
                    
                    // 获取销售信息
                    BigDecimal unitPrice = HBaseUtils.getBigDecimal(result, "sale_info", "unitPrice");
                    Long quantity = HBaseUtils.getLong(result, "sale_info", "quantity");
                    BigDecimal totalPrice = HBaseUtils.getBigDecimal(result, "sale_info", "totalPrice");
                    
                    // 打印结果（一行输出）
                    System.out.println(rowKey + "\t" + fruitName + "\t" + fruitType + "\t" + 
                                     fruitOrigin + "\t" + 
                                     (unitPrice != null ? unitPrice.toPlainString() : "null") + "\t" + 
                                     quantity + "\t" + 
                                     (totalPrice != null ? totalPrice.toPlainString() : "null"));
                }
                System.out.println("共查询到 " + count + " 条符合条件的数据");
            }
        } catch (IOException e) {
            System.err.println("查询失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
            System.out.println("HBase 关闭连接");
        }
    }
}
