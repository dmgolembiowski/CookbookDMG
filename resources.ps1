$RGArray = 'Sandbox Admin'
$RType = 'Microsoft.Compute/disks', 'Microsoft.Storage/storageAccounts'
az account set -s 'POS Sandbox'
$resourceArr = az resource list | ConvertFrom-Json

Function finish_him($resource) {
    $n=$true

    foreach ($rg in $RGArray){

        if ($resource.ResourceGroup -like "*$rg*"){

            $n=$false

        }

    }

    foreach ($RT in $RType){

        if ($resource.type -like "*$RT*"){

            $n=$false

        }

    }

    return $n

}

           

foreach ($r in $resourceArr){

    $KillItDead = finish_him($r)

    if ($KillItDead){

        echo 'Killing with extreme prejudice ' $r.id

        az resource delete --id $r.id

    } else {

        echo $r.id ' has been spared'

    }

}
