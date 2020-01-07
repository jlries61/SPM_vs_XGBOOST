#!/usr/bin/perl
sub getind($%);
sub getval($\@\%);
sub mkindex(@);
sub putval($$\@\%);
sub readlist($);
sub readln($);
sub unquote(@);
sub writelist($@);
sub writeln($$);

#Set constants
$DLM = ",";
$DPV = "any_inj_dth";
$INFILE = "8.ex.InjuryDeath_data.csv";
$OUTFILE = "8.ex.InjuryDeath_data2.csv";

open STDIN, "<", $INFILE || die "Failure to open input file $INFILE $!\n";
open STDOUT, ">", $OUTFILE || die "Failure to open output file $OUTFILE $!\n";

@names = &unquote(&readlist(STDIN));
push @names, $DPV;
%index = &mkindex(@names);
&writelist(STDOUT, @names);

while (!eof(STDIN)) {
  my @field = &readlist(STDIN);
  my $injdeath = &getval("inj_dth", \@field, \%index);
  my $dpvval = $injdeath;
  if ($injdeath > 1) {$dpvval = 1}
  elsif ($injdeath < 0) {$dpvval = 0}
  &putval($DPV, $dpvval, \@field, \%index);
  &writelist(STDOUT, @field);
}

sub getind($%) {
  my ($name, %index) = @_;
  my $index = $index{$name};
  if (!defined($index)) {die}
  return $index;
}

sub getval($\@\%) {
  my ($name, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  return $$pbuf[$index];
}

sub mkindex(@) {
  my $nnames = @name = @_;
  my %index;
  for (my $i = 0; $i < $nnames; $i++) {
    $index{$name[$i]} = $i;
  }
  return %index;
}

sub putval($$\@\%) {
  my ($name, $value, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  $$pbuf[$index] = $value;
}

sub readlist($) {
  my ($fh) = @_;
  my $line = &readln($fh);
  return split($DLM, $line);
}

sub readln($) {
  my ($fh) = @_;
  my $line = <$fh>;
  chomp $line;
  return $line;
}

sub unquote(@) {
  my @outlist = ();
  foreach my $str (@_) {
    $str=~s/\"//g;
    push @outlist, $str;
  }
  return @outlist;
}

sub writelist($@) {
  my ($fh, @list) = @_;
  &writeln($fh, join($DLM, @list));
}

sub writeln($$) {
  my ($fh, $line) = @_;
  print $fh "$line\n";
}
