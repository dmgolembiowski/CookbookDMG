#!/iware/perl/bin/perl -w
# 1. Ensure $IWARE_HOME is set
# 2. Add $IWARE_HOME/lib/site_perl to @INC
# 3. Default the environment based on $IWARE_HOME
BEGIN { die "IWARE_HOME not set\n" unless $ENV{IWARE_HOME};}
use lib "$ENV{IWARE_HOME}/sap_lib/site_perl";

# Auto extract environment name from iware_home unless it is
# overridden by ENVIRONMENT environment variable (useful for testing).

my ($iware_env) = $ENV{ENVIRONMENT} || $ENV{IWARE_HOME} =~ m!/iware/(.+)!;

use strict;
use DBD::Oracle;
use LC::Constants;
use POSIX;
use File::Basename;

my $env_const     = new LC::Constants($iware_env);
my $sid           = $env_const->get('ORACLE_SID');
my $ro_user       = $env_const->get('RO_USER');
my $ro_pass       = $env_const->get('RO_PASS');

$ENV{'ORACLE_HOME'} = $env_const->get('ORACLE_HOME');
my $dbh =  DBI->connect("dbi:Oracle:$sid", $ro_user, $ro_pass);

# get the path of the script, and find a path relative to that directory

my $data_path = dirname($0) . "/../tmp";
die "Connection to database failed: $DBI::errstr" if $DBI::err;
my $handle = $dbh->prepare(<<EOSQL);

select s.site,
       w.lab_order_number,
       w.transaction_number,
       to_char(o.dispense_date, 'DD-MM-YYYY HH24:MI:SS') dispense_date
from LCBEAN.txn_order_lc o
join LCBEAN.txn_work_order_lc w
  on (o.store_code = w.torder_store_code and o.transaction_number = w.torder_transaction_number)
join eeis.store_v s on (o.store_code = s.store_code)
where trunc(o.dispense_date) = trunc(sysdate -1)

EOSQL

die "Database query prepare failed: $DBI::errstr" if $DBI::err;

# can do $handle->bind_param("name", value) to specify bind parameters here.

$handle->execute();
die "Database query execute failed: $DBI::errstr" if $DBI::err;

my $output_timestamp = POSIX::strftime "%Y%m%d", localtime;
my $output_file_name = "${data_path}/ENDispense${output_timestamp}.csv";

open(OUTPUT_FILE, ">${output_file_name}") or die "Could not open $output_file_name: $!";

my $row;
while ($row = $handle->fetchrow_arrayref) {
  print OUTPUT_FILE join(",",@{$row}) . "\n";
}
die "Fetching rows from database failed: $DBI::errstr" if $DBI::err;
close(OUTPUT_FILE);
