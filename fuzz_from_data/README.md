# Fuzz from data

## Configure apache server(version:2.4)

```bash
  cd /etc/apache2/sites-available/
  vim 000-default.conf
  
  # add follow lines to <virtualHost>...</virtualHost>
  LogLevel dumpio:trace7
  DumpIOInput On
  DumpIOOutput On
```

## You can see some detail logs

```bash
  cd /var/log/apache2/
  tail -f error.log
```

## Parse http logs from the error.log

```bash
cat error.log | cut -f8- -d':' | egrep -v ' [0-9]+ bytes$' | grep -v '^$' | cut -c2- | sed 's/\\r\\n//'
```

## Mutate the captured requests

```bash
python mutationTesting.py
```
