package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BigDecimalComparator;
import org.apache.hadoop.hbase.filter.FilterList;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 查看销售额高于2000或者产地为Yunnan的水果信息和销售信息
 */
public class HighSalesOrYunnanFilter {
    static Connection connection;
    static Table table;

    public static void main(String[] args) throws IOException {
        connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        table = connection.getTable(tableName);
        Scan scan = new Scan();

        // 过滤条件1：销售额 > 2000
        SingleColumnValueFilter totalPriceFilter = new SingleColumnValueFilter(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("totalPrice"),
                CompareOperator.GREATER,
                new BigDecimalComparator(new BigDecimal("2000")));

        // 过滤条件2：产地为Yunnan
        SingleColumnValueFilter originFilter = new SingleColumnValueFilter(
                Bytes.toBytes("fruit_info"),
                Bytes.toBytes("fruitOrigin"),
                CompareOperator.EQUAL,
                Bytes.toBytes("Yunnan"));

        // 使用FilterList组合两个过滤条件，MUST_PASS_ONE表示满足其中一个即可（OR条件）
        FilterList filterList = new FilterList(
                FilterList.Operator.MUST_PASS_ONE,
                totalPriceFilter,
                originFilter);

        // 将过滤器设置到scan
        scan.setFilter(filterList);

        System.out.println("========== 销售额 > 2000 或 产地为Yunnan 的水果信息 ==========");
        for (Result result : table.getScanner(scan)) {
            // 获取Rowkey
            String rowkey = Bytes.toString(result.getRow());

            // 获取水果信息
            String fruitName = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName")));
            String fruitType = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType")));
            String fruitOrigin = Bytes.toString(result.getValue(
                    Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin")));

            // 获取销售信息
            String unitPriceStr = Bytes.toString(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice")));
            BigDecimal unitPrice = new BigDecimal(unitPriceStr);

            Long quantity = Bytes.toLong(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("quantity")));

            String totalPriceStr = Bytes.toString(result.getValue(
                    Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice")));
            BigDecimal totalPrice = new BigDecimal(totalPriceStr);

            System.out.println("水果编号:" + rowkey +
                    "，水果名:" + fruitName +
                    "，水果类型:" + fruitType +
                    "，水果产地:" + fruitOrigin +
                    "，单价：" + unitPrice +
                    "，销量：" + quantity +
                    "，销售额：" + totalPrice);
        }

        HBaseConnect.closeConnection();
    }
}
