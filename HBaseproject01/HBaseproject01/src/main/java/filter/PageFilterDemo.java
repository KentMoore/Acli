package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.PageFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;

public class PageFilterDemo {
        static Connection connection;
        static Table table;

        public static void main(String[] args) throws IOException {
            connection = HBaseConnect.getConnection();
            TableName tableName = TableName.valueOf("commodity1:fruit_table");
            table = connection.getTable(tableName);

//            Scan scan = new Scan();
            // 跟踪最新行的行键
            byte[] lastRowkey = null;
            int page = 1;
            // 创建PageFilter过滤器,一个参数：分页的指定行数
            PageFilter pageFilter = new PageFilter(8);
            while(true) {
                System.out.println("----------------第"+page+"页-------------------");
                page++;
                // 创建Scan
                Scan scan = new Scan();
                // 将分页过滤器配置scan
                scan.setFilter(pageFilter);
                if(lastRowkey != null) {
                    scan.withStartRow(lastRowkey,false);
                }
                int count = 0;
                for(Result result:table.getScanner(scan)) {
                    String rowkey = Bytes.toString(result.getRow());

                    // 获取水果信息（字符串）
                    String fruitName = Bytes.toString(result.getValue(
                            Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName")));
                    String fruitType = Bytes.toString(result.getValue(
                            Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType")));
                    String fruitOrigin = Bytes.toString(result.getValue(
                            Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin")));

                    // ====== 关键修改 ======
                    // unitPrice: 写入是String，读取也用String，再转BigDecimal
                    String unitPriceStr = Bytes.toString(result.getValue(
                            Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice")));
                    BigDecimal unitPrice = new BigDecimal(unitPriceStr);

                    // quantity: 写入是Long，读取也用Long ✓
                    Long quantity = Bytes.toLong(result.getValue(
                            Bytes.toBytes("sale_info"), Bytes.toBytes("quantity")));

                    // totalPrice: 写入是String，读取也用String，再转BigDecimal
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
                    count++;
                    lastRowkey = result.getRow();
                }
                if(count < 8) {
                    break;
                }
            }
            HBaseConnect.closeConnection();


    }
}
