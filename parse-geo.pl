#!/usr/bin/perl
use Geo::IP;

#my $gi = Geo::IP->new(GEOIP_STANDARD);
# https://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
# https://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
# https://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
#my $gcity = Geo::IP->open('/usr/share/GeoIP/GeoLiteCity.dat' , GEOIP_STANDARD );
#my $gcountry = Geo::IP->open('/usr/share/GeoIP/GeoIP.dat' , GEOIP_STANDARD );
my $gasn = Geo::IP->open('/usr/share/GeoIP/GeoIPASNum.dat' , GEOIP_STANDARD );
my $recordcity,$city,$country,$ip;

while (<>) {
$ip=$_; 
chomp($ip);
if ($ip =~ /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/) {
$country = $gcountry->country_code_by_addr($ip);
#$asn = $gasn->name_by_addr($ip);
# $recordcity = $gcity->record_by_addr($ip);

#$country=$recordcity->country_code;
#$city=$recordcity->city;

printf "$ip;$asn\n";
#printf "$ip;$country\n";
}
}
