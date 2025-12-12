package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptor;

import java.io.IOException;

public class DescStudentInfo {
    public static void main(String[] args) throws IOException {
        Connection conn = HBaseConnect.getConnection();
        Admin admin = conn.getAdmin();

        TableName t = TableName.valueOf("commodity1:fruit_info");
        if (!admin.tableExists(t)) {
            System.out.println("not found");
            admin.close();
            HBaseConnect.closeConnection();
            return;
        }

        TableDescriptor td = admin.getDescriptor(t);
        System.out.println("table=" + td.getTableName().getNameAsString()
                + " enabled=" + admin.isTableEnabled(t)
                + " readOnly=" + td.isReadOnly());

        for (ColumnFamilyDescriptor cfd : td.getColumnFamilies()) {
            System.out.println(
                    "cf=" + cfd.getNameAsString()
                            + " maxVer=" + cfd.getMaxVersions()
                            + " minVer=" + cfd.getMinVersions()
                            + " ttl=" + cfd.getTimeToLive()
                            + " compress=" + cfd.getCompressionType().getName()
                            + " bloom=" + cfd.getBloomFilterType());
        }

        System.out.println("regions=" + admin.getRegions(t).size());

        admin.close();
        HBaseConnect.closeConnection();
    }
}