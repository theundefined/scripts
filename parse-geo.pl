#!/usr/bin/perl
use Geo::IP;

#my $gi = Geo::IP->new(GEOIP_STANDARD);
my $gcity = Geo::IP->open('/usr/share/GeoIP/GeoLiteCity.dat' , GEOIP_STANDARD );
my $gcountry = Geo::IP->open('/usr/share/GeoIP/GeoIP.dat' , GEOIP_STANDARD );
my $gasn = Geo::IP->open('/usr/share/GeoIP/GeoIPASNum.dat' , GEOIP_STANDARD );
my $recordcity,$city,$country,$ip;

while (<>) {
$ip=$_; 
chomp($ip);
if ($ip =~ /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/) {
$country = $gcountry->country_code_by_addr($ip);
$asn = $gasn->org_by_addr($ip);
$recordcity = $gcity->record_by_addr($ip);

$country=$recordcity->country_code;
$city=$recordcity->city;

printf "$ip;$country;$city;$asn\n";
}
}
