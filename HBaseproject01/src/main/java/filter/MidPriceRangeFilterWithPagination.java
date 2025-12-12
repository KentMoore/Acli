package filter;

import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BigDecimalComparator;
import org.apache.hadoop.hbase.filter.FilterList;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;
import util.HBaseUtils;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 中等价格区间过滤器
 * 
 * 查询条件：
 * 1. 单价（unitPrice）>= 5
 * 2. 单价（unitPrice）<= 20
 */
public class MidPriceRangeFilterWithPagination {

    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();
        System.out.println("HBase 连接已创建");
        
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        try (Table table = connection.getTable(tableName)) {
            Scan scan = new Scan();
            
            // 创建过滤器列表（使用 AND 逻辑）
            FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);
            
            // 过滤器1：单价 >= 5
            SingleColumnValueFilter minPriceFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("unitPrice"),
                    CompareOperator.GREATER_OR_EQUAL,
                    new BigDecimalComparator(BigDecimal.valueOf(5)));
            
            // 过滤器2：单价 <= 20
            SingleColumnValueFilter maxPriceFilter = new SingleColumnValueFilter(
                    Bytes.toBytes("sale_info"),
                    Bytes.toBytes("unitPrice"),
                    CompareOperator.LESS_OR_EQUAL,
                    new BigDecimalComparator(BigDecimal.valueOf(20)));
            
            // 将两个过滤器添加到过滤器列表
            filterList.addFilter(minPriceFilter);
            filterList.addFilter(maxPriceFilter);
            
            // 配置过滤器到 scan
            scan.setFilter(filterList);

            System.out.println("=== 查询结果：单价 >= 5 且 <= 20 ===");
            System.out.println("RowKey\tfruitName\tfruitType\tfruitOrigin\tunitPrice\tquantity\ttotalPrice");
            System.out.println("----------------------------------------------");
            
            try (ResultScanner scanner = table.getScanner(scan)) {
                int count = 0;
                int pageCount = 0;
                for (Result result : scanner) {
                    count++;
                    
                    // 每5条数据输出一个分页标记
                    if (count > 1 && (count - 1) % 5 == 0) {
                        pageCount++;
                        System.out.println("------------------- 第 " + pageCount + " 页 -------------------");
                    }
                    
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
                
                // 输出最后一页的标记
                if (count > 0) {
                    pageCount++;
                    System.out.println("------------------- 第 " + pageCount + " 页 -------------------");
                }
                
                System.out.println("共查询到 " + count + " 条符合条件的数据，共 " + pageCount + " 页");
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
